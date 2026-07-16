#!/usr/bin/env python3
"""Classify repos in dim_repo via Claude Haiku 4.5, skipping unchanged descriptions.

Usage: ANTHROPIC_API_KEY=sk-... python3 classify.py
"""
import hashlib
import json
import os
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "whats_building.db")
MODEL = "claude-haiku-4-5"
API_URL = "https://api.anthropic.com/v1/messages"

# Haiku 4.5 pricing, per million tokens — verify against current docs before trusting cost totals.
PRICE_PER_MTOK_INPUT = 1.00
PRICE_PER_MTOK_OUTPUT = 5.00

SYSTEM_PROMPT = """You classify GitHub repositories based on their name and description.

For each repo, output:
- category: the single best-fit technical category for what the repo IS or DOES
- domain: the single best-fit product/business vertical the repo serves
- is_ai_built_or_related: whether the repo is itself an AI/LLM tool, or is fundamentally about AI/LLM functionality
- confidence: your confidence in this classification, 0.0-1.0

category and domain are independent axes — a repo can be category=web-app and
domain=fintech at the same time. Pick exactly one value for each from the lists below.

Categories (technical shape of the repo):
- ai-meta-tooling: tools FOR building/running AI systems (agent frameworks, MCP servers, LLM IDEs, prompt tooling, agent skills)
- ai-application: a product or app that uses AI/LLMs as a feature, but isn't itself AI infrastructure
- dev-tooling: developer tools, CLIs, libraries, frameworks not centered on AI
- web-app: web applications or services
- mobile-app: mobile applications
- desktop-app: desktop/native applications
- data-infra: databases, pipelines, data engineering
- game: games or game engines
- other: doesn't fit above, or insufficient information

Domains (product/business vertical the repo serves). For developer-facing repos,
distinguish dev-tooling-general / ai-agent-ecosystem / infra-ops by what phase of
building software the end-user is in — writing code, building an AI agent, or
operating a live system — not by the repo's own technical shape (that's category):
- fintech: money, payments, banking, budgeting, invoicing, trading
- productivity: task/project management, workflow automation
- note-taking-pkm: notes, personal knowledge management, wikis
- health-fitness: health tracking, fitness, medical
- education: learning, teaching, courses
- e-commerce: online retail, marketplaces, storefronts
- social-communication: chat, social networks, messaging
- gaming-entertainment: games, media consumption, entertainment
- security: security tooling, auth, pentesting, privacy
- data-analytics: data pipelines, BI, analytics, visualization
- content-media: content creation, publishing, media editing
- dev-tooling-general: helps someone write, test, or ship application code (linters, CLIs, testing libraries, build tools, general-purpose frameworks)
- ai-agent-ecosystem: helps someone build or operate an AI/LLM agent specifically (agent skills, MCP servers, agent orchestration/frameworks, prompt tooling)
- infra-ops: helps someone deploy, monitor, or run systems already in production (Kubernetes, SRE, cloud infra, CI/CD, observability)
- docs-reference: curated lists, awesome-lists, guides, tutorials, documentation repos with no runnable product
- other: doesn't fit above, or insufficient information

Rules for ambiguous cases:
- A repo ABOUT the AI tooling ecosystem (e.g. "a collection of MCP servers", "agent orchestration framework") is ai-meta-tooling AND is_ai_built_or_related=true — do not undercount these just because they aren't themselves an LLM wrapper.
- A repo that merely mentions "GPT" or "AI" once, in a non-central way (e.g. a non-English description where AI is incidental, not the point), should NOT be flagged is_ai_built_or_related=true. Judge centrality, not keyword presence.
- If description is missing or empty, use only the repo name and any topics provided. Lower confidence accordingly — do not guess category with high confidence from a name alone unless it's unambiguous (e.g. "gpt-pdf-chat").
- Non-English descriptions: translate mentally and classify on meaning, not surface tokens.

Output strictly via the provided tool. No free text."""

TOOL = {
    "name": "repo_classification",
    "description": "Classify a GitHub repository.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["ai-meta-tooling", "ai-application", "dev-tooling", "web-app",
                          "mobile-app", "desktop-app", "data-infra", "game", "other"],
            },
            "domain": {
                "type": "string",
                "enum": ["fintech", "productivity", "note-taking-pkm", "health-fitness",
                          "education", "e-commerce", "social-communication",
                          "gaming-entertainment", "security", "data-analytics",
                          "content-media", "dev-tooling-general", "ai-agent-ecosystem",
                          "infra-ops", "docs-reference", "other"],
            },
            "is_ai_built_or_related": {"type": "boolean"},
            "confidence": {"type": "number"},
        },
        "required": ["category", "domain", "is_ai_built_or_related", "confidence"],
    },
}


def fetch_repos(con):
    cur = con.cursor()
    cur.execute("""
        SELECT r.repo_id, r.name, r.description, r.language,
               GROUP_CONCAT(t.topic_name, ', ') AS topics
        FROM dim_repo r
        LEFT JOIN bridge_repo_topic bt ON bt.repo_id = r.repo_id
        LEFT JOIN dim_topic t ON t.topic_id = bt.topic_id
        GROUP BY r.repo_id
    """)
    return cur.fetchall()


def existing_hash(con, repo_id):
    cur = con.cursor()
    cur.execute("SELECT description_hash FROM fact_repo_classification WHERE repo_id = ?", (repo_id,))
    row = cur.fetchone()
    return row[0] if row else None


def call_claude(api_key, name, description, language, topics):
    message = (
        f"Repo name: {name}\n"
        f"Description: {description or '(none)'}\n"
        f"Language: {language or '(none)'}\n"
        f"Topics: {topics or 'none'}"
    )
    body = {
        "model": MODEL,
        "max_tokens": 256,
        "system": SYSTEM_PROMPT,
        "tools": [TOOL],
        "tool_choice": {"type": "tool", "name": "repo_classification"},
        "messages": [{"role": "user", "content": message}],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(DB_PATH)
    repos = fetch_repos(con)

    classified, skipped, errors = 0, 0, 0
    total_input_tokens, total_output_tokens = 0, 0
    category_counts = {}
    domain_counts = {}

    for repo_id, name, description, language, topics in repos:
        desc_hash = hashlib.sha256((description or "").encode()).hexdigest()
        if existing_hash(con, repo_id) == desc_hash:
            skipped += 1
            continue

        try:
            resp = call_claude(api_key, name, description, language, topics)
        except Exception as e:
            print(f"ERROR classifying {name} ({repo_id}): {e}", file=sys.stderr)
            errors += 1
            continue

        tool_use = next((b for b in resp["content"] if b["type"] == "tool_use"), None)
        if tool_use is None:
            print(f"ERROR: no tool_use in response for {name}", file=sys.stderr)
            errors += 1
            continue

        result = tool_use["input"]
        usage = resp["usage"]
        total_input_tokens += usage["input_tokens"]
        total_output_tokens += usage["output_tokens"]
        category_counts[result["category"]] = category_counts.get(result["category"], 0) + 1
        domain_counts[result["domain"]] = domain_counts.get(result["domain"], 0) + 1

        con.execute("""
            INSERT INTO fact_repo_classification
                (repo_id, category, domain, is_ai_built_or_related, confidence, description_hash, classified_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(repo_id) DO UPDATE SET
                category=excluded.category,
                domain=excluded.domain,
                is_ai_built_or_related=excluded.is_ai_built_or_related,
                confidence=excluded.confidence,
                description_hash=excluded.description_hash,
                classified_at=excluded.classified_at
        """, (
            repo_id,
            result["category"],
            result["domain"],
            int(result["is_ai_built_or_related"]),
            str(result["confidence"]),
            desc_hash,
            datetime.now(timezone.utc).isoformat(),
        ))
        con.commit()
        classified += 1
        print(f"{name}: {result['category']} / {result['domain']} / ai={result['is_ai_built_or_related']} / conf={result['confidence']}")

    con.close()

    input_cost = total_input_tokens / 1_000_000 * PRICE_PER_MTOK_INPUT
    output_cost = total_output_tokens / 1_000_000 * PRICE_PER_MTOK_OUTPUT

    print("\n--- Summary ---")
    print(f"Classified: {classified}, skipped (unchanged): {skipped}, errors: {errors}")
    print(f"Category breakdown: {category_counts}")
    print(f"Domain breakdown: {domain_counts}")
    print(f"Tokens: {total_input_tokens} in / {total_output_tokens} out")
    print(f"Est. cost: ${input_cost + output_cost:.4f} (input ${input_cost:.4f} + output ${output_cost:.4f})")


if __name__ == "__main__":
    main()
