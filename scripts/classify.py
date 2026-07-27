#!/usr/bin/env python3
"""Classify repos in dim_repo via Claude Haiku 4.5, skipping unchanged descriptions.

Batches ~BATCH_SIZE repos per model call so the ~1,500-token system prompt is
amortized instead of re-paid per repo (Haiku's cache minimum is 4096 tokens, so
prompt caching does not apply — batching is the cost lever). Two modes:

  python3 classify.py            synchronous (daily incremental, small N)
  python3 classify.py --batch    Message Batches API, 50% off (one-time bulk)

Reads ANTHROPIC_TOKEN from env or .env.
"""
import argparse
import hashlib
import json
import os
import random
import sqlite3
import sys
import time
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "whats_building.db")
MODEL = "claude-haiku-4-5"
API = "https://api.anthropic.com/v1"
BATCH_SIZE = 20
# Chunks per Batch API submission. The full run is ~146 MB of requests; splitting
# keeps each POST ~22 MB and lands results in the DB incrementally.
SUBMIT_CHUNKS = 2000

# Haiku 4.5 pricing per Mtok. Batch API halves both. Verify before trusting totals.
PRICE_IN, PRICE_OUT = 1.00, 5.00

# The taxonomy lives in dim_taxonomy (single source of truth). CATEGORIES,
# DOMAINS and the two bullet blocks below are loaded from the DB at runtime by
# load_taxonomy(); nothing here is hardcoded.
CATEGORIES, DOMAINS = [], []

PROMPT_TEMPLATE = """You classify GitHub repositories from their name and description.

Two independent axes; never answer both with the same idea:
- category = what FORM the repo takes (its shape as software)
- domain   = what SUBJECT the repo is about (its field)
Pick exactly one value for each from the lists below.

An MCP server library is category=library-sdk, domain=ai-agents-mcp. A curated
list of fintech APIs is category=docs-reference, domain=fintech.

Categories (the FORM the repo takes — never the subject matter):
{categories}

Domains (the SUBJECT the repo is about — never its form). Always choose the most
specific applicable field. Do not fall back to a broad value because the repo is
developer-facing; developer tools still have a subject (a Kotlin logging library
is observability, a shading language is graphics-3d):
{domains}

Rules for ambiguous cases:
- unknown vs other: use `unknown` ONLY when there is too little information to judge (missing/empty/vague description and an uninformative name). Use `other` when you understand the repo perfectly well but no listed value fits. These are different failures — do not substitute one for the other.
- Prefer a specific value over an escape value. Only use unknown/other after genuinely considering every listed option.
- Classify by what the repo itself PROVIDES, not the host it plugs into or the framework it targets. A visual theme/skin is domain=ui-frontend even if it themes a DevOps dashboard or a game. A helper inside a web framework takes its FUNCTIONAL domain (getting a client IP is networking; rate limiting or CORS is security/networking; an ORM binding is data-analytics) — "targets a web framework" is not by itself ui-frontend. ui-frontend is only for repos whose subject IS the visual/UI layer.
- is_ai_built_or_related: set true whenever the repo itself provides or depends on AI/LLM functionality (including a fintech app whose core feature is an LLM); it is NOT the same as having an AI domain, and a curated list counts only if it is itself about AI. Leave it false for an AI-adjacent repo with no AI, or one that merely mentions "GPT"/"AI" in passing — judge centrality, not keyword presence.
- If description is missing or empty, use only the repo name and any topics provided. Lower confidence accordingly, and prefer `unknown` over a high-confidence guess.
- Non-English descriptions: translate mentally and classify on meaning, not surface tokens.

Return one classification per repo, echoing its repo_id exactly. confidence is 0.0-1.0."""

# Built from the DB by load_taxonomy(). strict:True makes the enums binding —
# without it they are advisory and the model invents values.
SYSTEM_PROMPT = ""
TOOL = None


def load_taxonomy(con):
    """Populate CATEGORIES, DOMAINS, SYSTEM_PROMPT and TOOL from dim_taxonomy."""
    global CATEGORIES, DOMAINS, SYSTEM_PROMPT, TOOL
    rows = con.execute(
        "SELECT axis, slug, description FROM dim_taxonomy ORDER BY axis, sort_order"
    ).fetchall()
    if not rows:
        sys.exit("dim_taxonomy is empty — seed it with sql/seed_taxonomy.sql")
    cats = [(s, d) for a, s, d in rows if a == "category"]
    doms = [(s, d) for a, s, d in rows if a == "domain"]
    CATEGORIES = [s for s, _ in cats]
    DOMAINS = [s for s, _ in doms]
    SYSTEM_PROMPT = PROMPT_TEMPLATE.format(
        categories="\n".join(f"- {s}: {d}" for s, d in cats),
        domains="\n".join(f"- {s}: {d}" for s, d in doms),
    )
    TOOL = {
        "name": "classify_repos",
        "description": "Classify a batch of GitHub repositories.",
        "strict": True,
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
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["classifications"],
            "additionalProperties": False,
        },
    }


def load_key():
    key = os.environ.get("ANTHROPIC_TOKEN")
    if key:
        return key
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("ANTHROPIC_TOKEN="):
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
    groups = [chunks[i:i + SUBMIT_CHUNKS] for i in range(0, len(chunks), SUBMIT_CHUNKS)]
    for g, group in enumerate(groups):
        requests = [{"custom_id": f"g{g}c{i}", "params": params(c)}
                    for i, c in enumerate(group)]
        batch = post("/messages/batches", {"requests": requests})
        bid = batch["id"]
        print(f"  batch {g+1}/{len(groups)} submitted {bid} ({len(requests)} requests)")
        while True:
            b = json.loads(get(f"/messages/batches/{bid}"))
            if b["processing_status"] == "ended":
                break
            print(f"  processing… {b.get('request_counts', {})}")
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
        print(f"  batch {g+1}/{len(groups)} written  classified={stats['done']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", action="store_true", help="use Message Batches API (bulk)")
    ap.add_argument("--limit", type=int, help="classify a random sample of N repos")
    ap.add_argument("--seed", type=int, default=0, help="sampling seed (reproducible)")
    args = ap.parse_args()

    if not API_KEY:
        print("ANTHROPIC_TOKEN not set (env or .env)", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA busy_timeout=15000")
    load_taxonomy(con)
    repos = repos_to_classify(con)
    print(f"{len(repos)} repos to classify ({'batch' if args.batch else 'sync'} mode)")
    if not repos:
        return
    if args.limit and args.limit < len(repos):
        random.seed(args.seed)
        repos = random.sample(repos, args.limit)
        print(f"sampling {len(repos)} at random (seed={args.seed})")
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
