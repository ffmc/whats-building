#!/usr/bin/env python3
"""Classify repos in dim_repo via Claude Haiku 4.5, skipping unchanged descriptions.

Batches ~BATCH_SIZE repos per model call so the ~1,500-token system prompt is
amortized instead of re-paid per repo (Haiku's cache minimum is 4096 tokens, so
prompt caching does not apply — batching is the cost lever). Two modes:

  python3 classify.py            synchronous (daily incremental, small N)
  python3 classify.py --batch    Message Batches API, 50% off (one-time bulk)

Reads ANTHROPIC_API_KEY from env or .env.
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
import urllib.request
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "whats_building.db")
MODEL = "claude-haiku-4-5"
API = "https://api.anthropic.com/v1"
BATCH_SIZE = 20

# Haiku 4.5 pricing per Mtok. Batch API halves both. Verify before trusting totals.
PRICE_IN, PRICE_OUT = 1.00, 5.00

CATEGORIES = ["ai-meta-tooling", "ai-application", "dev-tooling", "web-app",
              "mobile-app", "desktop-app", "data-infra", "game", "other"]
DOMAINS = ["fintech", "productivity", "note-taking-pkm", "health-fitness",
           "education", "e-commerce", "social-communication", "gaming-entertainment",
           "security", "data-analytics", "content-media", "dev-tooling-general",
           "ai-agent-ecosystem", "infra-ops", "docs-reference", "other"]

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

You will receive a numbered list of repos. Return one classification per repo,
echoing its repo_id exactly. Output strictly via the provided tool. No free text."""

TOOL = {
    "name": "classify_repos",
    "description": "Classify a batch of GitHub repositories.",
    "input_schema": {
        "type": "object",
        "properties": {
            "classifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "repo_id": {"type": "integer"},
                        "category": {"type": "string", "enum": CATEGORIES},
                        "domain": {"type": "string", "enum": DOMAINS},
                        "is_ai_built_or_related": {"type": "boolean"},
                        "confidence": {"type": "number"},
                    },
                    "required": ["repo_id", "category", "domain",
                                 "is_ai_built_or_related", "confidence"],
                },
            },
        },
        "required": ["classifications"],
    },
}


def load_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    env = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


API_KEY = load_key()
HEADERS = {"content-type": "application/json", "x-api-key": API_KEY or "",
           "anthropic-version": "2023-06-01"}


def post(path, body):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(),
                                 headers=HEADERS, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def get(path_or_url):
    url = path_or_url if path_or_url.startswith("http") else API + path_or_url
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return r.read()


def repos_to_classify(con):
    """Repos whose description_hash changed or that have no classification yet."""
    rows = con.execute("""
        SELECT r.repo_id, r.name, r.description, r.language,
               GROUP_CONCAT(t.topic_name, ', ') AS topics
        FROM dim_repo r
        LEFT JOIN bridge_repo_topic bt ON bt.repo_id = r.repo_id
        LEFT JOIN dim_topic t ON t.topic_id = bt.topic_id
        GROUP BY r.repo_id
    """).fetchall()
    existing = dict(con.execute(
        "SELECT repo_id, description_hash FROM fact_repo_classification").fetchall())
    out = []
    for repo_id, name, desc, lang, topics in rows:
        h = hashlib.sha256((desc or "").encode()).hexdigest()
        if existing.get(repo_id) != h:
            out.append({"repo_id": repo_id, "name": name, "description": desc,
                        "language": lang, "topics": topics, "hash": h})
    return out


def user_message(chunk):
    lines = ["Classify these repositories:\n"]
    for r in chunk:
        lines.append(
            f"repo_id={r['repo_id']} | name: {r['name']} | "
            f"description: {r['description'] or '(none)'} | "
            f"language: {r['language'] or '(none)'} | topics: {r['topics'] or 'none'}"
        )
    return "\n".join(lines)


def params(chunk):
    return {
        "model": MODEL,
        "max_tokens": 4096,
        "system": SYSTEM_PROMPT,
        "tools": [TOOL],
        "tool_choice": {"type": "tool", "name": "classify_repos"},
        "messages": [{"role": "user", "content": user_message(chunk)}],
    }


def tool_output(message):
    block = next((b for b in message["content"] if b["type"] == "tool_use"), None)
    return block["input"]["classifications"] if block else []


def write(con, classifications, hash_by_id, stats):
    now = datetime.now(timezone.utc).isoformat()
    for c in classifications:
        rid = c["repo_id"]
        if rid not in hash_by_id:
            continue
        con.execute("""
            INSERT INTO fact_repo_classification
                (repo_id, category, domain, is_ai_built_or_related, confidence,
                 description_hash, classified_at)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(repo_id) DO UPDATE SET
                category=excluded.category, domain=excluded.domain,
                is_ai_built_or_related=excluded.is_ai_built_or_related,
                confidence=excluded.confidence,
                description_hash=excluded.description_hash,
                classified_at=excluded.classified_at
        """, (rid, c["category"], c["domain"], int(c["is_ai_built_or_related"]),
              str(c["confidence"]), hash_by_id[rid], now))
        stats["cat"][c["category"]] = stats["cat"].get(c["category"], 0) + 1
    con.commit()
    stats["done"] += len(classifications)


def run_sync(con, chunks, hash_by_id, stats):
    for i, chunk in enumerate(chunks):
        resp = post("/messages", params(chunk))
        stats["in"] += resp["usage"]["input_tokens"]
        stats["out"] += resp["usage"]["output_tokens"]
        write(con, tool_output(resp), hash_by_id, stats)
        print(f"  chunk {i+1}/{len(chunks)}  classified={stats['done']}")


def run_batch(con, chunks, hash_by_id, stats):
    requests = [{"custom_id": f"c{i}", "params": params(c)} for i, c in enumerate(chunks)]
    batch = post("/messages/batches", {"requests": requests})
    bid = batch["id"]
    print(f"  submitted batch {bid} ({len(requests)} requests)")
    while True:
        b = json.loads(get(f"/messages/batches/{bid}"))
        if b["processing_status"] == "ended":
            break
        counts = b.get("request_counts", {})
        print(f"  processing… {counts}")
        time.sleep(30)
    for line in get(b["results_url"]).splitlines():
        result = json.loads(line)
        if result["result"]["type"] == "succeeded":
            msg = result["result"]["message"]
            stats["in"] += msg["usage"]["input_tokens"]
            stats["out"] += msg["usage"]["output_tokens"]
            write(con, tool_output(msg), hash_by_id, stats)
        else:
            print(f"  {result['custom_id']}: {result['result']['type']}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", action="store_true", help="use Message Batches API (bulk)")
    args = ap.parse_args()

    if not API_KEY:
        print("ANTHROPIC_API_KEY not set (env or .env)", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA busy_timeout=15000")
    repos = repos_to_classify(con)
    print(f"{len(repos)} repos to classify ({'batch' if args.batch else 'sync'} mode)")
    if not repos:
        return
    hash_by_id = {r["repo_id"]: r["hash"] for r in repos}
    chunks = [repos[i:i + BATCH_SIZE] for i in range(0, len(repos), BATCH_SIZE)]

    stats = {"done": 0, "in": 0, "out": 0, "cat": {}}
    mult = 0.5 if args.batch else 1.0
    (run_batch if args.batch else run_sync)(con, chunks, hash_by_id, stats)
    con.close()

    cost = (stats["in"] / 1e6 * PRICE_IN + stats["out"] / 1e6 * PRICE_OUT) * mult
    print(f"\nClassified {stats['done']} repos. Categories: {stats['cat']}")
    print(f"Tokens: {stats['in']} in / {stats['out']} out. Est. cost: ${cost:.2f}")


if __name__ == "__main__":
    main()
