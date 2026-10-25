#!/usr/bin/env python3
"""Generic daily-drop hub page builder (replaces per-date build scripts).

Reads ~/workspace/redbubble/designs/daily/<DATE>/<1|2|3>/metadata.json + PNG,
writes oddjack-site daily pages + 1920x1920 web JPGs, appends rows to the
website-url-map, and regenerates the sitemap.

Usage:
  build_daily.py <DATE> [--urls urls.json] [--no-sitemap] [--no-map]
  urls.json: {"<slug>": {"rb": "...", "kofi": "..."}} — re-run with live URLs
  after the publisher run to replace coming-soon CTAs.
"""
import html, json, os, re, sys

SITE = "https://oddjack0.github.io/oddjack-art"
REPO = "/home/hatch/workspace/oddjack-site"
OUT_BASE = os.path.join(REPO, "daily")
IMG_DIR = os.path.join(REPO, "images")
DES = "/home/hatch/workspace/redbubble/designs/daily"
MAP = "/home/hatch/workspace/goals/multiply-income-streams/niche-expansion/website-url-map.md"


def slugify(title):
    s = title.lower()
    s = re.sub(r"['\u2019]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def esc(s):
    return html.escape(s, quote=True)


def main():
    date = sys.argv[1]
    urls = {}
    if "--urls" in sys.argv:
        urls = json.load(open(sys.argv[sys.argv.index("--urls") + 1]))
    do_sitemap = "--no-sitemap" not in sys.argv
    do_map = "--no-map" not in sys.argv

    from PIL import Image
    css = open(os.path.join(OUT_BASE, "2026-10-16-personal-space-grumpy-armadillo",
                            "index.html")).read().split("<style>")[1].split("</style>")[0]

    # previous day's designs for the related grid (best effort)
    prev = sorted(os.listdir(DES))
    prev = [d for d in prev if d < date]
    recent = []
    if prev:
        pd = prev[-1]
        for n in ("1", "2", "3"):
            mp = os.path.join(DES, pd, n, "metadata.json")
            if os.path.exists(mp):
                m = json.load(open(mp))
                sl = f"{pd}-{slugify(m['title'])}"
                recent.append({"slug": sl, "webimg": f"daily-{sl}-web.jpg",
                               "title": m["title"]})

    designs = []
    for n in ("1", "2", "3"):
        ddir = os.path.join(DES, date, n)
        m = json.load(open(os.path.join(ddir, "metadata.json")))
        pngs = [f for f in os.listdir(ddir) if f.lower().endswith(".png")]
        assert pngs, f"no PNG in {ddir}"
        src = os.path.join(ddir, sorted(pngs)[0])
        slug = f"{date}-{slugify(m['title'])}"
        u = urls.get(slug, {})
        designs.append({"title": m["title"], "slug": slug, "src": src,
                        "blurb": m.get("description", ""),
                        "tags": ", ".join(m.get("tags", [])),
                        "webimg": f"daily-{slug}-web.jpg",
                        "rb": u.get("rb"), "kofi": u.get("kofi")})

    header = open(os.path.join(REPO, "daily", "2026-10-24-i-brought-the-sides-grumpy-turkey-at-the-table", "index.html")).read()
    footer = header.split("</main>")[1].split("</body>")[0]

    for d in designs:
        web = os.path.join(IMG_DIR, d["webimg"])
        if not os.path.exists(web):
            im = Image.open(d["src"]).convert("RGB")
            w, h = im.size
            s = min(w, h)
            im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
            im = im.resize((1920, 1920), Image.LANCZOS)
            im.save(web, "JPEG", quality=88)
            print("web img", d["webimg"])
        page_url = f"{SITE}/daily/{d['slug']}/"
        img_url = f"{SITE}/images/{d['webimg']}"
        short = esc(d["blurb"][:150] + "…")
        kofi = (f'<p><a class="btn" href="{d["kofi"]}" rel="noopener">Download on Ko-fi — $2</a></p>'
                if d["kofi"] else
                '<p class="note">Digital download coming soon — the $2 Ko-fi listing is still being published. Check back shortly.</p>')
        rb = (f'<p><a class="btn rb" href="{d["rb"]}" rel="noopener">Merch on Redbubble</a></p>'
              if d["rb"] else
              '<p class="note">Redbubble merch coming soon — the listing is still being published. Check back shortly.</p>')
        ticks = ["Original art by Odd Jack O.M.T.",
                 "Merch live now on Redbubble tees, hoodies & stickers" if d["rb"] else "Redbubble merch coming soon",
                 "$2 fixed-price digital download on Ko-fi" if d["kofi"] else "$2 digital download coming soon on Ko-fi"]
        tick_html = "\n".join(f"<li>{esc(i)}</li>" for i in ticks)
        cards = []
        for o in designs:
            if o["slug"] == d["slug"]:
                continue
            cards.append(f'<a class="card" href="{SITE}/daily/{o["slug"]}/"><img src="{SITE}/images/{o["webimg"]}" alt="{esc(o["title"])}" loading="lazy"><div class="t">{esc(o["title"])}</div><div class="p">$2.00</div></a>')
        for r in recent:
            cards.append(f'<a class="card" href="{SITE}/daily/{r["slug"]}/"><img src="{SITE}/images/{r["webimg"]}" alt="{esc(r["title"])}" loading="lazy"><div class="t">{esc(r["title"])}</div><div class="p">$2.00</div></a>')
        grid = "".join(cards)
        ld_url = d["rb"] or d["kofi"] or page_url
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(d["title"])} — Daily Drop | Odd-jack</title>
<meta name="description" content="{short}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(d["title"])} — Daily Drop | Odd-jack">
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
    "availability": "https://schema.org/InStock", "url": "{ld_url}"}}
}}
</script></head>
<body>
{header.split("<main")[0].split("<body>")[1]}
<main class="wrap">
<p class="crumb"><a href="{SITE}/">Home</a> › <a href="{SITE}/daily/">Daily Drops</a> › {esc(d["title"])}</p>
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
<h2>More daily drops</h2>
<div class="grid">{grid}</div>
</main>{footer}
</body>
</html>
"""
        outdir = os.path.join(OUT_BASE, d["slug"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w") as f:
            f.write(page)
        print("wrote", d["slug"], "| rb:", d["rb"] or "PENDING", "| kofi:", d["kofi"] or "PENDING")

    if do_map:
        with open(MAP, "a") as f:
            for d in designs:
                f.write(f"| {date} | {d['title']} | {SITE}/daily/{d['slug']}/ |\n")
        print("map appended")
    if do_sitemap:
        import subprocess
        subprocess.run(["python3", os.path.join(REPO, "regen-sitemap.py")], check=True)
        print("sitemap regenerated")


if __name__ == "__main__":
    main()
