#!/usr/bin/env python3
"""Inline the JSON data into site/index.html to produce a single openable file.

The served page fetch()es site/data/*.json, which browsers block over file://.
This bakes summary.json + taxonomy.json into a <script> block and rewrites the
loader to read them, so whats-building.html opens by double-click, no server.
Re-run after aggregate.py or any edit to site/index.html.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "site", "index.html"), encoding="utf-8").read()
data = {
    "summary": json.load(open(os.path.join(ROOT, "site/data/summary.json"), encoding="utf-8")),
    "taxonomy": json.load(open(os.path.join(ROOT, "site/data/taxonomy.json"), encoding="utf-8")),
}

inline = ("<script>window.__DATA__ = "
          + json.dumps(data, separators=(",", ":"), ensure_ascii=False)
          + ";</script>\n<script>")

# Replace the Promise.all([...fetch...]) opener with a resolve of the inlined data.
out = src.replace("<script>\nconst F = new Intl.NumberFormat", inline + "\nconst F = new Intl.NumberFormat", 1)
out = re.sub(
    r"Promise\.all\(\[\s*fetch\('data/summary\.json'\)\.then\(r => r\.json\(\)\),\s*"
    r"fetch\('data/taxonomy\.json'\)\.then\(r => r\.json\(\)\)\s*\]\)\.then\(\(\[d, tax\]\) => \{",
    "Promise.resolve([window.__DATA__.summary, window.__DATA__.taxonomy]).then(([d, tax]) => {",
    out,
)

dest = os.path.join(ROOT, "whats-building.html")
open(dest, "w", encoding="utf-8").write(out)
kb = os.path.getsize(dest) / 1024
assert "window.__DATA__.summary" in out, "loader rewrite failed"
assert "fetch('data/" not in out, "a fetch() survived — file:// will break"
print(f"wrote {dest}  {kb:.0f} KB")
