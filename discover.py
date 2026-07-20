#!/usr/bin/env python3
"""Discover repos via GitHub Search API into dim_repo.

Filter: created 2021-07-19..today, stars >= 50, non-fork.
Beats the 1000-results-per-query cap by adaptively splitting the created-date
range until each slice is under 1000, then paginating it. Idempotent
(INSERT OR IGNORE on repo_id), so re-running resumes.

Optional: GITHUB_TOKEN in env (30 req/min vs 10 unauthenticated).
Usage: [GITHUB_TOKEN=ghp_...] python3 discover.py [--start YYYY-MM-DD] [--end YYYY-MM-DD]
"""
import argparse
import os
import sqlite3
import sys
import time
from datetime import date, datetime, timedelta, timezone

import requests

DB_PATH = os.path.join(os.path.dirname(__file__), "whats_building.db")
API = "https://api.github.com/search/repositories"
STARS_MIN = 50
WINDOW_START = date(2021, 7, 19)
PER_PAGE = 100

def _load_token():
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    env = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("GITHUB_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


TOKEN = _load_token()
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"
REQ_DELAY = 2.1 if TOKEN else 6.1  # respect 30/min (auth) or 10/min (unauth)

session = requests.Session()
session.headers.update(HEADERS)


def get(params):
    """One Search request with rate-limit handling."""
    while True:
        try:
            r = session.get(API, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"  network error ({e.__class__.__name__}), retrying in 10s", file=sys.stderr)
            time.sleep(10)
            continue
        if r.status_code == 200:
            time.sleep(REQ_DELAY)
            return r.json()
        if r.status_code in (403, 429):
            reset = r.headers.get("X-RateLimit-Reset")
            retry = r.headers.get("Retry-After")
            if retry:
                wait = int(retry)
            elif reset:
                wait = max(1, int(reset) - int(time.time())) + 1
            else:
                wait = 60
            print(f"  rate-limited, sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        if r.status_code >= 500:
            print(f"  {r.status_code} transient, retrying in 10s", file=sys.stderr)
            time.sleep(10)
            continue
        r.raise_for_status()


def q(lo, hi):
    return f"created:{lo}..{hi} stars:>={STARS_MIN} fork:false"


def count(lo, hi):
    return get({"q": q(lo, hi), "per_page": 1})["total_count"]


def insert(con, items):
    now = datetime.now(timezone.utc).isoformat()
    n = 0
    for it in items:
        cur = con.execute(
            """INSERT OR IGNORE INTO dim_repo
               (repo_id, node_id, full_name, owner, owner_type, name, description,
                homepage, language, license, is_fork, is_template, default_branch,
                size_kb, created_at, pushed_at, archived, first_seen_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (it["id"], it["node_id"], it["full_name"], it["owner"]["login"],
             it["owner"]["type"], it["name"], it.get("description"),
             it.get("homepage"), it.get("language"),
             (it.get("license") or {}).get("spdx_id"),
             int(it["fork"]), int(it["is_template"]), it.get("default_branch"),
             it.get("size"), it["created_at"], it.get("pushed_at"),
             int(it["archived"]), now),
        )
        if cur.rowcount:
            n += 1
        for topic in it.get("topics", []):
            con.execute("INSERT OR IGNORE INTO dim_topic (topic_name) VALUES (?)", (topic,))
            con.execute(
                """INSERT OR IGNORE INTO bridge_repo_topic (repo_id, topic_id)
                   SELECT ?, topic_id FROM dim_topic WHERE topic_name = ?""",
                (it["id"], topic),
            )
    con.commit()
    return n


def paginate(con, lo, hi, total, state):
    pages = min(10, -(-total // PER_PAGE))  # ceil, capped at API's 1000/100
    for page in range(1, pages + 1):
        data = get({"q": q(lo, hi), "per_page": PER_PAGE, "page": page,
                    "sort": "stars", "order": "desc"})
        state["new"] += insert(con, data["items"])
    state["done_repos"] += total
    print(f"  {lo}..{hi}: {total} repos  (total new: {state['new']})")


def crawl(con, lo, hi, state):
    total = count(lo, hi)
    if total == 0:
        return
    if total > 1000 and lo < hi:
        mid = lo + (hi - lo) // 2
        crawl(con, lo, mid, state)
        crawl(con, mid + timedelta(days=1), hi, state)
    else:
        if total > 1000:
            print(f"  WARN single day {lo} has {total} > 1000; only top 1000 by stars",
                  file=sys.stderr)
        paginate(con, lo, hi, total, state)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=WINDOW_START.isoformat())
    ap.add_argument("--end", default=date.today().isoformat())
    args = ap.parse_args()

    lo = date.fromisoformat(args.start)
    hi = date.fromisoformat(args.end)
    print(f"auth: {'token' if TOKEN else 'UNAUTHENTICATED (10/min)'} | "
          f"range {lo}..{hi} | stars>={STARS_MIN} fork:false")

    con = sqlite3.connect(DB_PATH)
    state = {"new": 0, "done_repos": 0}
    t0 = time.time()
    crawl(con, lo, hi, state)
    con.close()
    print(f"\nDone. {state['new']} new repos in {(time.time()-t0)/60:.1f} min "
          f"({state['done_repos']} matched incl. already-present).")


if __name__ == "__main__":
    main()
