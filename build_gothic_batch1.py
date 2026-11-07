#!/usr/bin/env python3
"""Gothic Tarot batch 1 hub page builder (one-off for 2026-11-07).

Reads gothic-batch1-metadata.json + gothic-batch1-urls.json from the goal
hidden_files dir, writes oddjack-site gothic-tarot/<slug>/ pages + web JPGs
(portrait fit, NOT square-cropped — tarot cards are 1120x2240), appends rows
to the website-url-map, and regenerates the sitemap.

Adapted from build_daily.py's page template (same CSS/header/footer source
pages, same dual-CTA layout); section is "Gothic Tarot", related grid is the
other 18 batch-1 cards.
"""
import html
import json
import os
import subprocess
import sys

SITE = "https://oddjack0.github.io/oddjack-art"
REPO = "/home/hatch/workspace/oddjack-site"
OUT_BASE = os.path.join(REPO, "gothic-tarot")
IMG_DIR = os.path.join(REPO, "images")
SRC_DIR = "/home/hatch/workspace/websites/moonphase-tarot/gothic-tarot/batch1-majors"
META = "/home/hatch/workspace/goals/multiply-income-streams/hidden_files/gothic-batch1-metadata.json"
URLS = "/home/hatch/workspace/goals/multiply-income-streams/hidden_files/gothic-batch1-urls.json"
MAP = "/home/hatch/workspace/goals/multiply-income-streams/niche-expansion/website-url-map.md"
DATE = "2026-11-07"


def esc(s):
    return html.escape(s, quote=True)


def main():
    from PIL import Image

    cards = json.load(open(META))["cards"]
    urls = json.load(open(URLS))
    assert len(cards) == 19, f"expected 19 cards, got {len(cards)}"
    for c in cards:
        key = c["file"][:-4]  # file stem, e.g. gothic-00-fool
        u = urls.get(key)
        assert u and u.get("rb") and u.get("kofi"), f"missing URLs for {key}"

    css = open(os.path.join(REPO, "daily",
                            "2026-10-16-personal-space-grumpy-armadillo",
                            "index.html")).read().split("<style>")[1].split("</style>")[0]
    header = open(os.path.join(REPO, "daily",
                               "2026-10-24-i-brought-the-sides-grumpy-turkey-at-the-table",
                               "index.html")).read()
    footer = header.split("</main>")[1].split("</body>")[0]

    designs = []
    for c in cards:
        key = c["file"][:-4]
        u = urls[key]
        designs.append({"title": c["title"], "slug": c["slug"], "src": os.path.join(SRC_DIR, c["file"]),
                        "blurb": c["description"], "tags": ", ".join(c["tags"]),
                        "webimg": f"gothic-tarot-{c['slug']}-web.jpg",
                        "rb": u["rb"], "kofi": u["kofi"]})

    for d in designs:
        web = os.path.join(IMG_DIR, d["webimg"])
        if not os.path.exists(web):
            im = Image.open(d["src"]).convert("RGB")
            # portrait fit within 1280x1920 (no square crop — cards are tall)
            im.thumbnail((1280, 1920), Image.LANCZOS)
            im.save(web, "JPEG", quality=88)
            print("web img", d["webimg"], im.size)
        page_url = f"{SITE}/gothic-tarot/{d['slug']}/"
        img_url = f"{SITE}/images/{d['webimg']}"
        short = esc(d["blurb"][:150] + "…")
        kofi = (f'<p><a class="btn" href="{d["kofi"]}" rel="noopener">Download on Ko-fi — $2</a></p>')
        rb = (f'<p><a class="btn rb" href="{d["rb"]}" rel="noopener">Merch on Redbubble</a></p>')
        ticks = ["Original art by Odd Jack O.M.T.",
                 "Merch live now on Redbubble tees, hoodies & stickers",
                 "$2 fixed-price digital download on Ko-fi"]
        tick_html = "\n".join(f"<li>{esc(i)}</li>" for i in ticks)
        cards_html = []
        for o in designs:
            if o["slug"] == d["slug"]:
                continue
            cards_html.append(f'<a class="card" href="{SITE}/gothic-tarot/{o["slug"]}/"><img src="{SITE}/images/{o["webimg"]}" alt="{esc(o["title"])}" loading="lazy"><div class="t">{esc(o["title"])}</div><div class="p">$2.00</div></a>')
        grid = "".join(cards_html)
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(d["title"])} — Gothic Tarot | Odd-jack</title>
<meta name="description" content="{short}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(d["title"])} — Gothic Tarot | Odd-jack">
<meta property="og:description" content="{short}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{img_url}">
<style>{css}</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {json.dumps(d["title"])},
  "image": "{img_url}",
  "description": {json.dumps(d["blurb"][:160] + "…")},
  "brand": {{"@type": "Brand", "name": "Odd-jack"}},
  "offers": {{"@type": "Offer", "priceCurrency": "USD", "price": "2.0",
    "availability": "https://schema.org/InStock", "url": "{d["kofi"]}"}}
}}
</script></head>
<body>
{header.split("<main")[0].split("<body>")[1]}
<main class="wrap">
<p class="crumb"><a href="{SITE}/">Home</a> › <a href="{SITE}/gothic-tarot/">Gothic Tarot</a> › {esc(d["title"])}</p>
<div class="product">
<div><img src="{img_url}" alt="{esc(d["title"])}"></div>
<div>
<h1>{esc(d["title"])}</h1>
<p class="price">$2.00 <span class="sub">USD · fixed price</span></p>
{rb}
{kofi}
<ul class="tick">{tick_html}</ul>
<p>{esc(d["blurb"])}</p>
<p class="tags">Tags: {esc(d["tags"])}</p>
</div>
</div>
<h2>More Gothic tarot cards</h2>
<div class="grid">{grid}</div>
</main>{footer}
</body>
</html>
"""
        outdir = os.path.join(OUT_BASE, d["slug"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w") as f:
            f.write(page)
        print("wrote", d["slug"], "| rb:", d["rb"], "| kofi:", d["kofi"])

    # section index page (breadcrumb target for the 19 card pages)
    idx_cards = "".join(
        f'<a class="card" href="{SITE}/gothic-tarot/{o["slug"]}/"><img src="{SITE}/images/{o["webimg"]}" alt="{esc(o["title"])}" loading="lazy"><div class="t">{esc(o["title"])}</div><div class="p">$2.00</div></a>'
        for o in designs)
    idx_url = f"{SITE}/gothic-tarot/"
    idx_img = f"{SITE}/images/{designs[0]['webimg']}"
    idx = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gothic Tarot — Gothic Woodcut Tarot Card Art | Odd-jack</title>
<meta name="description" content="Gothic woodcut tarot card art: 19 Major Arcana in antique engraving style — dense black-ink crosshatching on aged parchment, bone-white highlights with faded gold and oxblood accents. $2 downloads on Ko-fi, merch on Redbubble.">
<link rel="canonical" href="{idx_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="Gothic Tarot — Gothic Woodcut Tarot Card Art | Odd-jack">
<meta property="og:description" content="19 Major Arcana in antique gothic woodcut engraving style. $2 downloads on Ko-fi, merch on Redbubble.">
<meta property="og:url" content="{idx_url}">
<meta property="og:image" content="{idx_img}">
<style>{css}</style>
</head>
<body>
{header.split("<main")[0].split("<body>")[1]}
<main class="wrap">
<p class="crumb"><a href="{SITE}/">Home</a> › Gothic Tarot</p>
<h1>Gothic Tarot</h1>
<p>Antique gothic woodcut engraving tarot art — dense black-ink crosshatching on aged parchment, bone-white highlights with faded gold and oxblood accents. 19 Major Arcana, each a $2 digital download on Ko-fi and merch on Redbubble.</p>
<div class="grid">{idx_cards}</div>
</main>{footer}
</body>
</html>
"""
    os.makedirs(OUT_BASE, exist_ok=True)
    with open(os.path.join(OUT_BASE, "index.html"), "w") as f:
        f.write(idx)
    print("wrote gothic-tarot index (19 cards)")

    with open(MAP, "a") as f:
        for d in designs:
            f.write(f"| {DATE} | {d['title']} | {SITE}/gothic-tarot/{d['slug']}/ |\n")
    print("map appended")

    subprocess.run(["python3", os.path.join(REPO, "regen-sitemap.py")], check=True)
    print("sitemap regenerated")


if __name__ == "__main__":
    main()
