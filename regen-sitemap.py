#!/usr/bin/env python3
"""Regenerate sitemap.xml by walking all index.html files.

Preserves the build.py entry format; priority is a heuristic based on path
depth so important hub pages keep higher priority. Idempotent.
"""
import os, re
import xml.dom.minidom

BASE = "https://oddjack0.github.io/oddjack-art"
ROOT = os.path.dirname(os.path.abspath(__file__))

# keep old lastmod values where the URL existed
old = {}
if os.path.exists(os.path.join(ROOT, "sitemap.xml")):
    txt = open(os.path.join(ROOT, "sitemap.xml")).read()
    for m in re.finditer(r"<url><loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", txt):
        old[m.group(1)] = m.group(2)
TODAY = "2026-10-02"

urls = []
for dirpath, _dn, fn in sorted(os.walk(ROOT)):
    if "index.html" not in fn:
        continue
    rel = os.path.relpath(dirpath, ROOT)
    path = "" if rel == "." else rel.replace(os.sep, "/") + "/"
    urls.append(BASE + "/" + path)

def priority(url):
    p = url.replace(BASE + "/", "").rstrip("/")
    depth = 0 if not p else p.count("/") + 1
    if not p:
        return "1.0"
    if p in ("guides", "niches", "daily", "halloween", "cat-wallpapers",
             "printable-wall-art", "sticker-art", "packs", "morbid-quotes",
             "bundles"):
        return "0.9"
    if depth == 1:
        return "0.8"
    return "0.7"

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    lm = old.get(u, TODAY)
    lines.append(f"  <url><loc>{u}</loc><lastmod>{lm}</lastmod>"
                 f"<changefreq>weekly</changefreq><priority>{priority(u)}</priority></url>")
lines.append("</urlset>")
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write("\n".join(lines) + "\n")

# verify: all previously-listed URLs still present
missing = [u for u in old if u not in set(urls)]
print(f"before={len(old)} after={len(urls)} missing={len(missing)}")
if missing:
    print("MISSING:", missing[:10])
xml.dom.minidom.parse(os.path.join(ROOT, "sitemap.xml"))
print("sitemap.xml is valid XML")
