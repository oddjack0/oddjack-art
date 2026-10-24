#!/usr/bin/env python3
"""Build daily-drop hub pages for 2026-10-24 (coming-soon CTAs; re-run with
live RB/Ko-fi URLs after the publisher run, like the 2026-10-22-23 builder).
Also generates 1920x1920 web JPGs in images/.
"""
import html, json, os
from PIL import Image

SITE = "https://oddjack0.github.io/oddjack-art"
OUT_BASE = "/home/hatch/workspace/oddjack-site/daily"
IMG_DIR = "/home/hatch/workspace/oddjack-site/images"
DES = "/home/hatch/workspace/redbubble/designs/daily"

DESIGNS = [
    {
        "date": "2026-10-24",
        "slug": "2026-10-24-i-brought-the-sides-grumpy-turkey-at-the-table",
        "title": "I Brought the Sides: Grumpy Turkey at the Table",
        "src": f"{DES}/2026-10-24/1/design-1.png",
        "blurb": "This grumpy turkey showed up to Thanksgiving dinner as a guest, not the main course, and he brought the sides to prove it. Deadpan, unbothered, and absolutely not on the menu.",
        "tags": "thanksgiving guest turkey, funny thanksgiving shirt, deadpan holiday humor, pilgrim hat bird, autumn feast art, sarcastic dinner guest, cute turkey cartoon, harvest season sticker, holiday potluck gift, november dinner party, grumpy bird illustration, turkey day humor, festive side dish, cartoon thanksgiving animal, funny fall shirt",
        "rb": None, "kofi": None,
    },
    {
        "date": "2026-10-24",
        "slug": "2026-10-24-i-told-you-so-smug-crow-on-a-skull",
        "title": "I Told You So: Smug Crow on a Skull",
        "src": f"{DES}/2026-10-24/2/design-2.png",
        "blurb": "This smug crow called it, and now he's perched on the proof with a grin that says everything. Dark humor, cute style, zero remorse.",
        "tags": "dark humor crow, gothic bird shirt, crow perched skull, spooky bird sticker, halloween crow art, edgy animal humor, black bird illustration, macabre cute design, goth animal gift, funny crow tee, skull perch cartoon, deadpan goth bird, october spooky sticker, dark cute animal, crow lover gift",
        "rb": None, "kofi": None,
    },
    {
        "date": "2026-10-24",
        "slug": "2026-10-24-plant-down-no-regrets-chaos-raccoon-on-the-loose",
        "title": "Plant Down, No Regrets: Chaos Raccoon on the Loose",
        "src": f"{DES}/2026-10-24/3/design-3.png",
        "blurb": "The plant is down, the soil is everywhere, and this chaos raccoon has absolutely no regrets. Feral energy, zero apologies, one very unbothered grin.",
        "tags": "feral raccoon meme, funny raccoon shirt, chaos animal sticker, trash panda humor, mischievous raccoon art, houseplant disaster gift, funny plant lover tee, zoomies animal cartoon, unhinged pet humor, knocked over pot, cute raccoon illustration, plant parent joke, messy animal sticker, funny raccoon gift, garden chaos cartoon",
        "rb": None, "kofi": None,
    },
]

# Filled in from the publisher run results (edit before re-running)
URLS = {
    "2026-10-24-i-brought-the-sides-grumpy-turkey-at-the-table": {"rb": "https://www.redbubble.com/shop/ap/185001228", "kofi": "https://ko-fi.com/s/aa0340f918"},
    "2026-10-24-i-told-you-so-smug-crow-on-a-skull": {"rb": "https://www.redbubble.com/shop/ap/185001390", "kofi": "https://ko-fi.com/s/a992cd0cc5"},
    "2026-10-24-plant-down-no-regrets-chaos-raccoon-on-the-loose": {"rb": "https://www.redbubble.com/shop/ap/185002140", "kofi": "https://ko-fi.com/s/beee578db9"},
}
for d in DESIGNS:
    if d["slug"] in URLS:
        u = URLS[d["slug"]]
        d["rb"] = u["rb"]
        d["kofi"] = u["kofi"]
    d["webimg"] = f"daily-{d['slug']}-web.jpg"


def esc(s):
    return html.escape(s, quote=True)


CSS = open("/home/hatch/workspace/oddjack-site/daily/2026-10-16-personal-space-grumpy-armadillo/index.html").read().split("<style>")[1].split("</style>")[0]


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


def related_grid(d, recent):
    cards = []
    for o in DESIGNS:
        if o["slug"] == d["slug"]:
            continue
        cards.append(
            f'<a class="card" href="{SITE}/daily/{o["slug"]}/">'
            f'<img src="{SITE}/images/{o["webimg"]}" alt="{esc(o["title"])}" loading="lazy">'
            f'<div class="t">{esc(o["title"])}</div><div class="p">$2.00</div></a>'
        )
    for r in recent:
        cards.append(
            f'<a class="card" href="{SITE}/daily/{r["slug"]}/">'
            f'<img src="{SITE}/images/{r["webimg"]}" alt="{esc(r["title"])}" loading="lazy">'
            f'<div class="t">{esc(r["title"])}</div><div class="p">$2.00</div></a>'
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

RECENT = [
    {"slug": "2026-10-23-sous-chef-of-sass-grumpy-cat-on-gravy-duty", "webimg": "daily-2026-10-23-sous-chef-of-sass-grumpy-cat-on-gravy-duty-web.jpg", "title": "Sous-Chef of Sass: Grumpy Cat on Gravy Duty"},
    {"slug": "2026-10-23-stuffing-critic-grumpy-goose-at-the-family-table", "webimg": "daily-2026-10-23-stuffing-critic-grumpy-goose-at-the-family-table-web.jpg", "title": "Stuffing Critic: Grumpy Goose at the Family Table"},
    {"slug": "2026-10-23-nap-season-sleepy-harvest-owl-skips-the-pie", "webimg": "daily-2026-10-23-nap-season-sleepy-harvest-owl-skips-the-pie-web.jpg", "title": "Nap Season: Sleepy Harvest Owl Skips the Pie"},
]

for d in DESIGNS:
    web = os.path.join(IMG_DIR, d["webimg"])
    if not os.path.exists(web):
        im = Image.open(d["src"]).convert("RGB")
        w, h = im.size
        s = min(w, h)
        im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
        im = im.resize((1920, 1920), Image.LANCZOS)
        im.save(web, "JPEG", quality=88)
        print("web img", d["webimg"])
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
<div class="grid">{related_grid(d, RECENT)}</div>
</main>{FOOTER}
</body>
</html>
"""
    outdir = os.path.join(OUT_BASE, slug)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(page)
    print("wrote", slug, "| rb:", d["rb"] or "PENDING", "| kofi:", d["kofi"] or "PENDING")
