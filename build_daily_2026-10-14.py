#!/usr/bin/env python3
"""Build daily-drop hub pages for 2026-10-14 from the 2026-10-13 template structure."""
import html, json, os

SITE = "https://oddjack0.github.io/oddjack-art"
IMG_DIR = "/home/hatch/workspace/oddjack-site/images"
OUT_BASE = "/home/hatch/workspace/oddjack-site/daily"

DESIGNS = [
    {
        "slug": "2026-10-14-grump-gobble",
        "title": "Grump Gobble",
        "webimg": "daily-2026-10-14-grump-gobble-web.jpg",
        "blurb": "He survived Thanksgiving and now Christmas wants a piece of him too. This gloriously grumpy turkey, tangled in holiday lights with gifts at his feet, is the mood for anyone who'd rather dodge the festivities entirely.",
        "tags": "funny turkey christmas shirt, santa hat turkey, turkey tangled in lights, deadpan bird humor, thanksgiving dinner bird, christmas lights animal, sassy bird gift, november dinner guest, cute bird illustration, yule bird apparel, flat cartoon turkey, cranky turkey xmas, funny bird shirt, holiday bird art, cute turkey design",
        "rb": None, "kofi": None,
    },
    {
        "slug": "2026-10-14-gothmas-but-make-it-flora",
        "title": "Gothmas, But Make It Flora",
        "webimg": "daily-2026-10-14-gothmas-but-make-it-flora-web.jpg",
        "blurb": "A gloriously unimpressed raven holds court among dark gothic poinsettias, thorny black rose branches, and matte black baubles. For everyone whose Christmas aesthetic leans more candlelit crypt than candy cane.",
        "tags": "gothic raven christmas, dark christmas bird, goth bird holiday, moody poinsettia art, dark botanical animal, creepy cute raven, black bird xmas, gothic holiday gift, dark academia bird, cranky crow art, goth christmas shirt, red candle bird, thorns and baubles, moody winter bird, dark christmas decor",
        "rb": None, "kofi": "https://ko-fi.com/s/2294cb2215",
    },
    {
        "slug": "2026-10-14-sorry-i-m-late-i-didn-t-want-to-come",
        "title": "Sorry I'm Late. I Didn't Want to Come.",
        "webimg": "daily-2026-10-14-sorry-i-m-late-i-didn-t-want-to-come-web.jpg",
        "blurb": "Peak reluctance, fur and all. This grumpy sloth hangs from his mossy branch with crumbs in his fur and zero intention of hurrying anywhere — the official mascot of every event you'd rather skip.",
        "tags": "grumpy sloth shirt, funny sloth gift, sassy sloth art, cranky animal humor, lazy sloth tee, introvert animal shirt, deadpan sloth design, cute grumpy animal, sloth hanging branch, antisocial sloth, funny lazy gift, cartoon sloth sticker, reluctant sloth art, mossy branch sloth, funny animal quote shirt",
        "rb": "https://www.redbubble.com/shop/ap/184726731",
        "kofi": "https://ko-fi.com/s/b5ba793b38",
    },
]

# Filled in from verification results (edit before running)
URLS = {
    "2026-10-14-grump-gobble": {"rb": None, "kofi": "https://ko-fi.com/s/99b640eb9c"},
    "2026-10-14-gothmas-but-make-it-flora": {"rb": None, "kofi": "https://ko-fi.com/s/2294cb2215"},
    "2026-10-14-sorry-i-m-late-i-didn-t-want-to-come": {"rb": "https://www.redbubble.com/shop/ap/184726731", "kofi": "https://ko-fi.com/s/b5ba793b38"},
}

for d in DESIGNS:
    u = URLS[d["slug"]]
    d["rb"] = u["rb"]
    d["kofi"] = u["kofi"]

def esc(s):
    return html.escape(s, quote=True)

CSS = open("/home/hatch/workspace/oddjack-site/daily/2026-10-13-merry-chaos-to-all/index.html").read().split("<style>")[1].split("</style>")[0]

def kofi_block(d):
    if d["kofi"]:
        return f'<p><a class="btn" href="{d["kofi"]}" rel="noopener">Download on Ko-fi — $2</a></p>'
    return '<p class="note">Digital download coming soon — the $2 Ko-fi listing is still being published. Check back shortly.</p>'

def rb_block(d):
    if d["rb"]:
        return f'<p><a class="btn rb" href="{d["rb"]}" rel="noopener">Merch on Redbubble</a></p>'
    return '<p class="note">Redbubble merch coming soon — the listing is still being published. Check back shortly.</p>'

def tick_items(d):
    items = ["Original art by Odd Jack O.M.T."]
    if d["rb"]:
        items.insert(0, "Merch live now on Redbubble tees, hoodies & stickers")
    else:
        items.insert(0, "Redbubble merch coming soon")
    if d["kofi"]:
        items.append("$2 fixed-price digital download on Ko-fi")
    else:
        items.append("$2 digital download coming soon on Ko-fi")
    return "\n".join(f"<li>{esc(i)}</li>" for i in items)

def related_grid(d):
    cards = []
    for o in DESIGNS:
        if o["slug"] == d["slug"]:
            continue
        cards.append(
            f'<a class="card" href="{SITE}/daily/{o["slug"]}/">'
            f'<img src="{SITE}/images/{o["webimg"]}" alt="{esc(o["title"])}" loading="lazy">'
            f'<div class="t">{esc(o["title"])}</div><div class="p">$2.00</div></a>'
        )
    # plus two recent older drops for depth
    cards.append(
        f'<a class="card" href="{SITE}/daily/2026-10-13-merry-chaos-to-all/">'
        f'<img src="{SITE}/images/daily-2026-10-13-merry-chaos-to-all-web.jpg" alt="Merry Chaos to All" loading="lazy">'
        f'<div class="t">Merry Chaos to All</div><div class="p">$2.00</div></a>'
    )
    cards.append(
        f'<a class="card" href="{SITE}/daily/2026-10-13-merry-christmas-stay-back/">'
        f'<img src="{SITE}/images/daily-2026-10-13-merry-christmas-stay-back-web.jpg" alt="Merry Christmas. Stay Back." loading="lazy">'
        f'<div class="t">Merry Christmas. Stay Back.</div><div class="p">$2.00</div></a>'
    )
    return "".join(cards)

FOOTER = """<footer><div class="wrap"><div class="fgrid">
<div><h4>Odd-jack Art</h4>
<p>Cute kawaii cats, elemental kitties, psychedelic art &amp; spooky Halloween drops by Odd Jack O.M.T. Instant-download phone wallpapers, printable wall art &amp; sticker packs.</p>
<div class="fcta"><a class="btn sm" href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a><a class="btn alt sm" href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Redbubble</a></div></div>
<div><h4>Shop</h4>
<a href="https://ko-fi.com/oddjack/shop" rel="noopener">All designs on Ko-fi</a>
<a href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Merch on Redbubble</a>
<a href="https://oddjack0.github.io/oddjack-art/bundles/">$16 Bundle Packs</a>
<a href="https://oddjack0.github.io/oddjack-art/calendars/">2027 Wall Calendars</a></div>
<div><h4>Explore</h4>
<a href="https://oddjack0.github.io/oddjack-art/niches/">Shop by Niche</a>
<a href="https://oddjack0.github.io/oddjack-art/daily/">Daily Drops</a>
<a href="https://oddjack0.github.io/oddjack-art/morbid-quotes/">Morbid Quotes</a>
<a href="https://oddjack0.github.io/oddjack-art/sitemap.xml">Sitemap</a></div>
</div><p class="copy">© 2026 Odd-jack. All art is original. Personal use only.</p></div></footer>"""

HEADER = """<header><div class="wrap"><a class="logo" href="https://oddjack0.github.io/oddjack-art/">ODD-JACK ART</a><nav><a href="https://oddjack0.github.io/oddjack-art/halloween/">Halloween</a><a href="https://oddjack0.github.io/oddjack-art/cat-wallpapers/">Wallpapers</a><a href="https://oddjack0.github.io/oddjack-art/printable-wall-art/">Prints</a><a href="https://oddjack0.github.io/oddjack-art/niches/">Niches</a><a href="https://oddjack0.github.io/oddjack-art/daily/">Daily Drops</a><a href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Redbubble</a><a href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a></nav></div></header>"""

for d in DESIGNS:
    slug = d["slug"]
    page_url = f"{SITE}/daily/{slug}/"
    img_url = f"{SITE}/images/{d['webimg']}"
    short = esc(d["blurb"][:150] + "…")
    ld_offer_url = d["rb"] or d["kofi"] or page_url
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
<style>{CSS}</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {json.dumps(d["title"])},
  "image": "{img_url}",
  "description": {json.dumps(d["blurb"][:160] + "…")},
  "brand": {{
    "@type": "Brand",
    "name": "Odd-jack"
  }},
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "2.0",
    "availability": "https://schema.org/InStock",
    "url": "{ld_offer_url}"
  }}
}}
</script></head>
<body>
{HEADER}
<main class="wrap">
<p class="crumb"><a href="{SITE}/">Home</a> › <a href="{SITE}/daily/">Daily Drops</a> › {esc(d["title"])}</p>
<div class="product">
<div><img src="{img_url}" alt="{esc(d["title"])}"></div>
<div>
<h1>{esc(d["title"])}</h1>
<p class="price">$2.00 <span class="sub">USD · fixed price</span></p>
{rb_block(d)}
{kofi_block(d)}
<ul class="tick">{tick_items(d)}</ul>
<p>{esc(d["blurb"])}</p>
<p class="tags">Tags: {esc(d["tags"])}</p>
</div>
</div>
<h2>More daily drops</h2>
<div class="grid">{related_grid(d)}</div>
</main>{FOOTER}
</body>
</html>
"""
    outdir = os.path.join(OUT_BASE, slug)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(page)
    print("wrote", slug, "| rb:", d["rb"] or "PENDING", "| kofi:", d["kofi"] or "PENDING")
