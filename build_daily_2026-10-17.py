#!/usr/bin/env python3
"""Build daily-drop hub pages for 2026-10-17 from the 2026-10-14 template structure."""
import html, json, os

SITE = "https://oddjack0.github.io/oddjack-art"
OUT_BASE = "/home/hatch/workspace/oddjack-site/daily"

DESIGNS = [
    {
        "slug": "2026-10-17-i-yam-what-i-yam",
        "title": "I Yam What I Yam",
        "webimg": "daily-2026-10-17-i-yam-what-i-yam-web.jpg",
        "blurb": "A grumpy sweet potato with vines for hair and arms crossed in full attitude, perched on a pile of marshmallows with falling autumn leaves. The Thanksgiving side-dish hero for friendsgiving matching tees — it knows it is the best dish on the table and it is not apologizing for it.",
        "tags": "grumpy sweet potato, funny yam character, thanksgiving food pun, friendsgiving humor, vegetable cartoon, cute food illustration, sassy side dish, autumn fall harvest, sticker art, marshmallow topped, kitchen decor gift, foodie joke, grumpy food character, cute cartoon design, harvest dinner funny",
        "rb": None, "kofi": None,
    },
    {
        "slug": "2026-10-17-salt-butter-attitude",
        "title": "Salt, Butter, Attitude",
        "webimg": "daily-2026-10-17-salt-butter-attitude-web.jpg",
        "blurb": "A grumpy fox chef in a tall chef's hat and polka-dot neckerchief, brandishing a wooden spoon and flipping a pan with a pat of butter. Dinner will be excellent — but he will absolutely judge your knife skills while making it.",
        "tags": "grumpy fox chef, funny fox cook, chef animal art, kitchen humor cartoon, cooking gift for chefs, cute fox illustration, frying pan toss, sassy kitchen decor, woodland animal art, culinary joke, restaurant worker gift, foodie cartoon character, cute sticker design, fox lover gift, kitchen wall art",
        "rb": None, "kofi": None,
    },
    {
        "slug": "2026-10-17-healing-era",
        "title": "Healing Era",
        "webimg": "daily-2026-10-17-healing-era-web.jpg",
        "blurb": "A grumpy capybara soaking in a steaming hot spring, lemon slice on its head, folded towel at the edge of the water — completely unimpressed by your wellness journey. It is healing, and it refuses to talk about it.",
        "tags": "grumpy capybara, capybara hot spring, hot spring soak, onsen bath animal, self care humor, mental wellness art, cozy bath cartoon, cute capybara illustration, relaxation gift, stress relief animal, spa day humor, kawaii animal art, lemon slice hat, steam bath cartoon, chill sticker design",
        "rb": None, "kofi": None,
    },
]

# Filled in from the publisher run results (edit before running)
URLS = {
    "2026-10-17-i-yam-what-i-yam": {"rb": "https://www.redbubble.com/shop/ap/184807646", "kofi": None},
    "2026-10-17-salt-butter-attitude": {"rb": "https://www.redbubble.com/shop/ap/184807692", "kofi": None},
    "2026-10-17-healing-era": {"rb": "https://www.redbubble.com/shop/ap/184807748", "kofi": "https://ko-fi.com/s/134a3a79d3"},
}

for d in DESIGNS:
    u = URLS[d["slug"]]
    d["rb"] = u["rb"]
    d["kofi"] = u["kofi"]


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
        f'<a class="card" href="{SITE}/daily/2026-10-16-personal-space-grumpy-armadillo/">'
        f'<img src="{SITE}/images/daily-2026-10-16-personal-space-grumpy-armadillo-web.jpg" alt="Personal Space: Grumpy Armadillo" loading="lazy">'
        f'<div class="t">Personal Space: Grumpy Armadillo</div><div class="p">$2.00</div></a>'
    )
    cards.append(
        f'<a class="card" href="{SITE}/daily/2026-10-16-pawsitive-vitals-only-grumpy-nurse-cat/">'
        f'<img src="{SITE}/images/daily-2026-10-16-pawsitive-vitals-only-grumpy-nurse-cat-web.jpg" alt="Pawsitive Vitals Only: Grumpy Nurse Cat" loading="lazy">'
        f'<div class="t">Pawsitive Vitals Only: Grumpy Nurse Cat</div><div class="p">$2.00</div></a>'
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
