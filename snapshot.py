#!/usr/bin/env python3
"""Snapshot repo metrics into fact_repo_metrics via GitHub GraphQL.

Reads dim_repo, fetches 100 repos/call by node_id (rename-proof), and inserts one
fact_repo_metrics row per repo for today at the given --tier. Also refreshes
dim_repo.pushed_at / archived / full_name in place (catches renames).

--tier anchor   foundation snapshot (default)
--tier weekly   weekly refresh (90d rolling retention)
--tier monthly  month-marker refresh (kept forever)

Requires GITHUB_TOKEN (.env). GraphQL needs auth.
Usage: python3 snapshot.py [--tier anchor|daily|monthly] [--limit N]
"""
import argparse
import os
import sqlite3
import sys
import time
from datetime import date

import requests

from discover import TOKEN  # reuse .env loader

DB_PATH = os.path.join(os.path.dirname(__file__), "whats_building.db")
GQL = "https://api.github.com/graphql"
CHUNK = 100
REQ_DELAY = 0.5

QUERY = """
query($ids: [ID!]!) {
  nodes(ids: $ids) {
    ... on Repository {
      databaseId
      nameWithOwner
      isArchived
      stargazerCount
      forkCount
      watchers { totalCount }
      issues(states: OPEN) { totalCount }
      pushedAt
    }
  }
}
"""


def gql(session, ids):
    while True:
        try:
            r = session.post(GQL, json={"query": QUERY, "variables": {"ids": ids}}, timeout=60)
        except requests.exceptions.RequestException as e:
            print(f"  network error ({e.__class__.__name__}), retrying in 10s", file=sys.stderr)
            time.sleep(10)
            continue
        if r.status_code == 200:
            body = r.json()
            if "errors" in body and not body.get("data"):
                print(f"  GraphQL errors: {body['errors'][:1]}", file=sys.stderr)
            time.sleep(REQ_DELAY)
            return body.get("data", {}).get("nodes", [])
        if r.status_code in (403, 429):
            wait = int(r.headers.get("Retry-After", 60))
            print(f"  rate-limited, sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        if r.status_code >= 500:
            print(f"  {r.status_code} transient, retrying in 10s", file=sys.stderr)
            time.sleep(10)
            continue
        r.raise_for_status()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default="anchor", choices=["anchor", "weekly", "monthly"])
    ap.add_argument("--limit", type=int, default=None, help="test on N repos")
    args = ap.parse_args()

    if not TOKEN:
        print("No GITHUB_TOKEN (.env) — GraphQL requires auth.", file=sys.stderr)
        sys.exit(1)

    snap = date.today().isoformat()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {TOKEN}"})

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA busy_timeout=15000")
    sql = "SELECT node_id, repo_id FROM dim_repo WHERE node_id IS NOT NULL"
    if args.limit:
        sql += f" LIMIT {args.limit}"
    rows = con.execute(sql).fetchall()
    id_map = {nid: rid for nid, rid in rows}
    node_ids = list(id_map)
    print(f"tier={args.tier} date={snap} | {len(node_ids)} repos to snapshot")

    inserted, missing = 0, 0
    for i in range(0, len(node_ids), CHUNK):
        batch = node_ids[i:i + CHUNK]
        nodes = gql(session, batch)
        for node in nodes:
            if not node:  # deleted/inaccessible repo
                missing += 1
                continue
            rid = node["databaseId"]
            cur = con.execute(
                """INSERT OR IGNORE INTO fact_repo_metrics
                   (repo_id, snapshot_date, tier, stargazers_count, forks_count,
                    watchers_count, open_issues_count)
                   VALUES (?,?,?,?,?,?,?)""",
                (rid, snap, args.tier, node["stargazerCount"], node["forkCount"],
                 node["watchers"]["totalCount"], node["issues"]["totalCount"]),
            )
            inserted += cur.rowcount
            con.execute(
                "UPDATE dim_repo SET pushed_at=?, archived=?, full_name=? WHERE repo_id=?",
                (node["pushedAt"], int(node["isArchived"]), node["nameWithOwner"], rid),
            )
        con.commit()
        if (i // CHUNK) % 10 == 0:
            print(f"  {min(i + CHUNK, len(node_ids))}/{len(node_ids)}  inserted={inserted}")

    con.close()
    print(f"\nDone. {inserted} metric rows ({args.tier}/{snap}); {missing} repos gone/inaccessible.")


if __name__ == "__main__":
    main()
