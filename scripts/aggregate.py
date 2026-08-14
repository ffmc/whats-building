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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "whats_building.db")
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


def taxonomy(con):
    """The category/domain definitions for the site legend and tooltips."""
    out = {"category": {}, "domain": {}}
    for axis, slug, label, desc, grp in con.execute(
        "SELECT axis, slug, label, description, grp FROM dim_taxonomy ORDER BY axis, sort_order"
    ):
        out[axis][slug] = {"label": label, "description": desc, "group": grp}
    return out


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
    confidence = dict(con.execute("""
        SELECT CASE WHEN CAST(confidence AS REAL) >= 0.8 THEN 'high'
                    WHEN CAST(confidence AS REAL) >= 0.6 THEN 'medium'
                    ELSE 'low' END,
               COUNT(*)
        FROM fact_repo_classification GROUP BY 1
    """))
    # 2021 and 2026 are partial (window opens 2021-07-19, anchor taken 2026-07-21);
    # the site marks them so the curve isn't read as a full-year drop.
    ai_by_year = [
        {"year": y, "total": tot, "ai": ai, "pct": round(100.0 * ai / tot, 1),
         "partial": y in ("2021", "2026")}
        for y, tot, ai in con.execute("""
            SELECT strftime('%Y', r.created_at), COUNT(*),
                   SUM(c.is_ai_built_or_related)
            FROM dim_repo r JOIN fact_repo_classification c USING (repo_id)
            GROUP BY 1 ORDER BY 1
        """)
    ]
    star_buckets = list(con.execute("""
        SELECT CASE WHEN stargazers_count < 100 THEN '50-99'
                    WHEN stargazers_count < 250 THEN '100-249'
                    WHEN stargazers_count < 500 THEN '250-499'
                    WHEN stargazers_count < 1000 THEN '500-999'
                    WHEN stargazers_count < 5000 THEN '1k-5k'
                    WHEN stargazers_count < 10000 THEN '5k-10k'
                    ELSE '10k+' END,
               COUNT(*)
        FROM fact_repo_metrics
        GROUP BY 1 ORDER BY MIN(stargazers_count)
    """))
    star_histogram = star_distribution(con)
    return {
        "total_repos": con.execute("SELECT COUNT(*) FROM dim_repo").fetchone()[0],
        "boom_date": BOOM_DATE,
        "confidence": confidence,
        "by_category": by_cat,
        "by_domain": by_domain,
        "created_by_month": by_month,
        "by_language": by_lang,
        "cohort": cohort,
        "ai_related_by_cohort": ai_by_cohort,
        "ai_by_year": ai_by_year,
        "star_buckets": star_buckets,
        "star_histogram": star_histogram,
    }


def star_distribution(con, bins=48):
    """Log-space histogram of star counts — raw bin counts with explicit
    edges, for a true histogram (not smoothed)."""
    import math

    stars = [row[0] for row in con.execute(
        "SELECT stargazers_count FROM fact_repo_metrics WHERE stargazers_count >= 50"
    )]
    log_stars = [math.log10(s) for s in stars]
    lo, hi = min(log_stars), max(log_stars)
    width = (hi - lo) / bins
    counts = [0] * bins
    for v in log_stars:
        idx = min(bins - 1, int((v - lo) / width))
        counts[idx] += 1

    return [
        {
            "starsMin": round(10 ** (lo + i * width)),
            "starsMax": round(10 ** (lo + (i + 1) * width)),
            "count": c,
        }
        for i, c in enumerate(counts)
    ]


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
               COALESCE(c.category, 'unclassified'), COALESCE(c.domain, 'unclassified'),
               c.confidence
        FROM dim_repo r LEFT JOIN fact_repo_classification c USING (repo_id)
    """).fetchall()
    by_cat = defaultdict(list)
    for rid, full_name, desc, lang, created, cat, domain, conf in rows:
        m = metrics.get(rid)
        if not m:
            continue
        entry = {"repo_id": rid, "full_name": full_name, "description": desc,
                 "language": lang, "created_at": created, "category": cat,
                 "domain": domain, "confidence": conf,
                 "url": f"https://github.com/{full_name}", **m}
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
    ap.add_argument("--out", default=os.path.join(ROOT, "site", "data"))
    args = ap.parse_args()

    con = sqlite3.connect(DB_PATH)
    metrics = latest_metrics(con)
    dump(os.path.join(args.out, "taxonomy.json"), taxonomy(con))
    dump(os.path.join(args.out, "summary.json"), summary(con))
    dump(os.path.join(args.out, "trends.json"), trends(con))
    for cat, entries in top_lists(con, metrics).items():
        dump(os.path.join(args.out, "top", f"{cat}.json"), entries)
    con.close()


if __name__ == "__main__":
    main()
