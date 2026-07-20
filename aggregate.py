#!/usr/bin/env python3
"""Aggregate the DB into static JSON for the website.

The only component that talks to a database — the site reads JSON only, so
swapping SQLite for a hosted store later changes this file and nothing else.

Usage: python3 aggregate.py [--out site/data]
"""
import argparse
import json
import os
import sqlite3
from collections import defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), "whats_building.db")
BOOM_DATE = "2022-11-30"  # ChatGPT launch: the pre/post cohort split
TOP_N = 100


def latest_metrics(con):
    return {
        rid: dict(zip(("stars", "forks", "watchers", "issues"), rest))
        for rid, *rest in con.execute("""
            SELECT m.repo_id, m.stargazers_count, m.forks_count,
                   m.watchers_count, m.open_issues_count
            FROM fact_repo_metrics m
            JOIN (SELECT repo_id, MAX(snapshot_date) d
                  FROM fact_repo_metrics GROUP BY repo_id) l
              ON l.repo_id = m.repo_id AND l.d = m.snapshot_date
        """)
    }


def summary(con):
    by_cat = dict(con.execute("""
        SELECT COALESCE(c.category, 'unclassified'), COUNT(*)
        FROM dim_repo r LEFT JOIN fact_repo_classification c USING (repo_id)
        GROUP BY 1 ORDER BY 2 DESC
    """))
    by_domain = dict(con.execute("""
        SELECT COALESCE(c.domain, 'unclassified'), COUNT(*)
        FROM dim_repo r LEFT JOIN fact_repo_classification c USING (repo_id)
        GROUP BY 1 ORDER BY 2 DESC
    """))
    by_month = dict(con.execute("""
        SELECT substr(created_at, 1, 7), COUNT(*)
        FROM dim_repo GROUP BY 1 ORDER BY 1
    """))
    by_lang = dict(con.execute("""
        SELECT COALESCE(language, 'unknown'), COUNT(*)
        FROM dim_repo GROUP BY 1 ORDER BY 2 DESC LIMIT 25
    """))
    cohort = dict(con.execute("""
        SELECT CASE WHEN created_at < ? THEN 'pre_boom' ELSE 'post_boom' END,
               COUNT(*)
        FROM dim_repo GROUP BY 1
    """, (BOOM_DATE,)))
    ai_by_cohort = dict(con.execute("""
        SELECT CASE WHEN r.created_at < ? THEN 'pre_boom' ELSE 'post_boom' END,
               SUM(c.is_ai_built_or_related)
        FROM dim_repo r JOIN fact_repo_classification c USING (repo_id)
        GROUP BY 1
    """, (BOOM_DATE,)))
    return {
        "total_repos": con.execute("SELECT COUNT(*) FROM dim_repo").fetchone()[0],
        "boom_date": BOOM_DATE,
        "by_category": by_cat,
        "by_domain": by_domain,
        "created_by_month": by_month,
        "by_language": by_lang,
        "cohort": cohort,
        "ai_related_by_cohort": ai_by_cohort,
    }


def trends(con):
    """Star/watcher totals per category per snapshot date."""
    out = defaultdict(dict)
    for cat, day, stars, watchers in con.execute("""
        SELECT COALESCE(c.category, 'unclassified'), m.snapshot_date,
               SUM(m.stargazers_count), SUM(m.watchers_count)
        FROM fact_repo_metrics m
        LEFT JOIN fact_repo_classification c USING (repo_id)
        GROUP BY 1, 2 ORDER BY 2
    """):
        out[cat][day] = {"stars": stars, "watchers": watchers}
    return out


def top_lists(con, metrics):
    rows = con.execute("""
        SELECT r.repo_id, r.full_name, r.description, r.language, r.created_at,
               COALESCE(c.category, 'unclassified'), COALESCE(c.domain, 'unclassified')
        FROM dim_repo r LEFT JOIN fact_repo_classification c USING (repo_id)
    """).fetchall()
    by_cat = defaultdict(list)
    for rid, full_name, desc, lang, created, cat, domain in rows:
        m = metrics.get(rid)
        if not m:
            continue
        entry = {"repo_id": rid, "full_name": full_name, "description": desc,
                 "language": lang, "created_at": created, "category": cat,
                 "domain": domain, "url": f"https://github.com/{full_name}", **m}
        by_cat[cat].append(entry)
        by_cat["all"].append(entry)
    return {cat: sorted(v, key=lambda e: e["stars"], reverse=True)[:TOP_N]
            for cat, v in by_cat.items()}


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"), ensure_ascii=False)
    print(f"  {path}  {os.path.getsize(path) / 1024:.0f} KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "site", "data"))
    args = ap.parse_args()

    con = sqlite3.connect(DB_PATH)
    metrics = latest_metrics(con)
    dump(os.path.join(args.out, "summary.json"), summary(con))
    dump(os.path.join(args.out, "trends.json"), trends(con))
    for cat, entries in top_lists(con, metrics).items():
        dump(os.path.join(args.out, "top", f"{cat}.json"), entries)
    con.close()


if __name__ == "__main__":
    main()
