#!/usr/bin/env python3
"""Insert 'Related gift guides' boxes into item pages + contextual guide links
into niche index pages. Idempotent: skips any file already containing 'guides/'.
"""
import os, re

BASE = "https://oddjack0.github.io/oddjack-art"
ROOT = os.path.dirname(os.path.abspath(__file__))

GUIDES = {
    "hub": ("Gift Guides", f"{BASE}/guides/"),
    "cat-christmas": ("Funny Cat Christmas Gifts for Cat Lovers",
                      f"{BASE}/guides/funny-cat-christmas-gifts/"),
    "fishing-dad": ("Funny Fishing Gifts for Dad",
                    f"{BASE}/guides/funny-fishing-gifts-for-dad/"),
    "book-lovers": ("Gifts for Book Lovers Who Are Obsessed with Reading",
                    f"{BASE}/guides/gifts-for-book-lovers/"),
    "faith": ("Christian Faith Gifts",
              f"{BASE}/guides/christian-faith-gifts/"),
    "trades": ("Blue Collar Gifts for Trades Workers",
               f"{BASE}/guides/blue-collar-trades-gifts/"),
    "stickers": ("Funny Cat Stickers & Digital Art",
                 f"{BASE}/guides/funny-cat-stickers-digital-art/"),
    "planners": ("Printable Planners That Actually Get Used",
                 f"{BASE}/guides/printable-planners/"),
    "notion": ("Notion Templates for Creators & Students",
               f"{BASE}/guides/notion-templates/"),
}

# niche dir -> item-page links + niche-index link
NICHE_GUIDES = {
    "trades-pride":     (["trades"], "trades"),
    "faith-apparel":    (["faith"], "faith"),
    "fishing-humor":    (["fishing-dad"], "fishing-dad"),
    "bookish":          (["book-lovers"], "book-lovers"),
    "planner-bundles":  (["planners"], "planners"),
    "notion-systems":   (["notion"], "notion"),
    "canva-kits":       (["hub"], "hub"),
    "america-250":      (["hub"], "hub"),
}
DAILY_LINKS = ["hub", "cat-christmas", "stickers"]


def box_html(keys):
    lis = "\n".join(
        f'<li><a href="{GUIDES[k][1]}">{GUIDES[k][0]}</a></li>' for k in keys)
    return (f'<section class="related-guides" style="margin:2rem 0">'
            f'<h2>Related gift guides</h2>\n<ul>\n{lis}\n</ul>\n</section>\n')


def insert_before_main(path, html):
    with open(path) as f:
        content = f.read()
    if "guides/" in content:
        return False  # already linked -> skip (idempotent)
    if "</main>" not in content:
        print(f"WARN: no </main> in {path}, skipped")
        return False
    content = content.replace("</main>", html + "</main>", 1)
    with open(path, "w") as f:
        f.write(content)
    return True


inserted, skipped = 0, 0

# 1. niche item pages
for niche, (keys, _niche_key) in NICHE_GUIDES.items():
    niche_dir = os.path.join(ROOT, "niches", niche)
    for name in sorted(os.listdir(niche_dir)):
        item = os.path.join(niche_dir, name, "index.html")
        if not os.path.isfile(item):
            continue
        if insert_before_main(item, box_html(keys)):
            inserted += 1
        else:
            skipped += 1

# 2. daily item pages
daily_dir = os.path.join(ROOT, "daily")
for name in sorted(os.listdir(daily_dir)):
    item = os.path.join(daily_dir, name, "index.html")
    if not os.path.isfile(item):
        continue
    if insert_before_main(item, box_html(DAILY_LINKS)):
        inserted += 1
    else:
        skipped += 1

# 3. niche index pages: one contextual link each
for niche, (_keys, idx_key) in NICHE_GUIDES.items():
    idx = os.path.join(ROOT, "niches", niche, "index.html")
    title, url = GUIDES[idx_key]
    blurb = (f'<p>Shopping for someone specific? Our '
             f'<a href="{url}">{title}</a> guide rounds up the best picks '
             f'worth giving.</p>\n')
    if insert_before_main(idx, blurb):
        inserted += 1
    else:
        skipped += 1

print(f"inserted into {inserted} files, skipped {skipped}")
