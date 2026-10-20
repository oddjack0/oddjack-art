#!/usr/bin/env python3
"""Build daily-drop hub pages for 2026-10-18 and 2026-10-19 (missing from the Oct 18/19 crew runs)."""
import html, json, os

SITE = "https://oddjack0.github.io/oddjack-art"
OUT_BASE = "/home/hatch/workspace/oddjack-site/daily"

DESIGNS = [
    {
        "slug": "2026-10-18-class-is-in-session-grumpy-goose-teacher",
        "title": "Class Is in Session: Grumpy Goose Teacher",
        "webimg": "daily-2026-10-18-class-is-in-session-grumpy-goose-teacher-web.jpg",
        "blurb": "This cranky goose runs the strictest classroom in the animal kingdom, pointer stick included. A perfect gag gift for teachers, professors, and anyone who corrects your grammar.",
        "tags": "funny professor gift, sarcastic educator humor, back to school animal, school comedy shirt, cartoon waterfowl art, school staff gag gift, deadpan bird humor, witty instructor present, academic satire tee, honking attitude design, chalkboard cartoon art, professor appreciation gift, snarky educator tee, bookish animal art, orange beak cartoon",
        "rb": "https://www.redbubble.com/shop/ap/184829853",
        "kofi": None,  # Oct-18 Ko-fi listings publish separately; filled after
    },
    {
        "slug": "2026-10-18-rest-is-a-hobby-grumpy-sloth-cocoa-nap",
        "title": "Rest Is a Hobby: Grumpy Sloth Cocoa Nap",
        "webimg": "daily-2026-10-18-rest-is-a-hobby-grumpy-sloth-cocoa-nap-web.jpg",
        "blurb": "This grumpy sloth has made resting a full-time hobby, cocoa mug firmly in claw. A cozy gift for introverts, slow-living fans, and anyone who naps like it is their job.",
        "tags": "mental wellness comfort gift, introvert comfort animal, blanket burrito art, lazy sunday design, cute slow animal, self care coffee gift, burnout recovery humor, hot drink cozy art, deadpan cute design, sleepy animal shirt, quiet time present, soft pastel cartoon, slow living design, relax and recharge, cranky blanket art",
        "rb": "https://www.redbubble.com/shop/ap/184829982",
        "kofi": None,
    },
    {
        "slug": "2026-10-18-love-language-distance-grumpy-skunk",
        "title": "Love Language: Distance \u2014 Grumpy Skunk",
        "webimg": "daily-2026-10-18-love-language-distance-grumpy-skunk-web.jpg",
        "blurb": "This grumpy skunk's love language is simple: keep your distance. A snarky gift for introverts, loners, and anyone who guards their personal space like treasure.",
        "tags": "funny boundaries gift, introvert relationship humor, snarky valentine alternative, crossed arms attitude, cute animal attitude, deadpan cartoon gift, dark humor animal shirt, sarcastic alone time design, boundaries humor tee, moody cartoon art, anti romance gift, pink kawaii design, prickly personality tee, goth cute animal, cranky critter design",
        "rb": "https://www.redbubble.com/shop/ap/184830167",
        "kofi": None,
    },
    {
        "slug": "2026-10-19-not-on-the-menu-grumpy-thanksgiving-turkey",
        "title": "Not on the Menu: Grumpy Thanksgiving Turkey",
        "webimg": "daily-2026-10-19-not-on-the-menu-grumpy-thanksgiving-turkey-web.jpg",
        "blurb": "This deadpan turkey has read the guest list and is not participating. A grumpy holiday-table standoff for everyone who would rather guard the pie than be it.",
        "tags": "funny harvest dinner shirt, sarcastic autumn animal, november feast humor, deadpan bird art, holiday table gag gift, poultry rebellion cartoon, fall feast sticker, pie guard illustration, cornucopia comedy tee, unimpressed animal design, autumn harvest humor, dinner dodger shirt, holiday dinner cartoon, orange pumpkin art, attitude animal gift",
        "rb": "https://www.redbubble.com/shop/ap/184857399",
        "kofi": "https://ko-fi.com/s/6b3f1dd7eb",
    },
    {
        "slug": "2026-10-19-cawffee-first-grumpy-goth-crow",
        "title": "Cawffee First: Grumpy Goth Crow",
        "webimg": "daily-2026-10-19-cawffee-first-grumpy-goth-crow-web.jpg",
        "blurb": "A perpetually unimpressed crow in a tiny witch hat guards his coffee with deadpan authority. For night owls, caffeine devotees, and anyone who answers before noon with a glare.",
        "tags": "funny witch bird shirt, dark humor animal tee, spooky halloween bird art, coffee lover sticker, deadpan halloween design, purple hat cartoon, caffeine addict gift, morbid cute art, edgy animal humor, october vibe tee, black bird illustration, morning cranky shirt, bats and spiders art, witch hat animal, spooky season sticker",
        "rb": "https://www.redbubble.com/shop/ap/184857485",
        "kofi": "https://ko-fi.com/s/bac25d72c4",
    },
    {
        "slug": "2026-10-19-same-honestly-dramatic-possum-plays-dead",
        "title": "Same, Honestly: Dramatic Possum Plays Dead",
        "webimg": "daily-2026-10-19-same-honestly-dramatic-possum-plays-dead-web.jpg",
        "blurb": "This possum has committed to the bit and is not getting up. A deadpan little drama queen for every burnout mood, bad Monday, and nap that lasted too long.",
        "tags": "feral animal meme shirt, unhinged wildlife humor, chaos animal art, lazy sunday tee, relatable burnout design, cartoon wildlife sticker, gen z animal humor, meme wildlife gift, deadpan animal illustration, overdramatic critter art, sleepy animal cartoon, mood meme design, cute but feral tee, sarcastic wildlife art, lazy animal humor",
        "rb": "https://www.redbubble.com/shop/ap/184857542",
        "kofi": "https://ko-fi.com/s/184ea6ab5d",
    },
]


def esc(s):
    return html.escape(s, quote=True)


CSS = open("/home/hatch/workspace/oddjack-site/daily/2026-10-16-personal-space-grumpy-armadillo/index.html").read().split("<style>")[1].split("</style>")[0]


def kofi_block(d):
    if d["kofi"]:
        return f'<p><a class="btn" href="{d["kofi"]}" rel="noopener">Download on Ko-fi \u2014 $2</a></p>'
    return '<p class="note">Digital download coming soon \u2014 the $2 Ko-fi listing is still being published. Check back shortly.</p>'


def rb_block(d):
    if d["rb"]:
        return f'<p><a class="btn rb" href="{d["rb"]}" rel="noopener">Merch on Redbubble</a></p>'
    return '<p class="note">Redbubble merch coming soon \u2014 the listing is still being published. Check back shortly.</p>'


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
</div><p class="copy">\u00a9 2026 Odd-jack. All art is original. Personal use only.</p></div></footer>"""

HEADER = """<header><div class="wrap"><a class="logo" href="https://oddjack0.github.io/oddjack-art/">ODD-JACK ART</a><nav><a href="https://oddjack0.github.io/oddjack-art/halloween/">Halloween</a><a href="https://oddjack0.github.io/oddjack-art/cat-wallpapers/">Wallpapers</a><a href="https://oddjack0.github.io/oddjack-art/printable-wall-art/">Prints</a><a href="https://oddjack0.github.io/oddjack-art/niches/">Niches</a><a href="https://oddjack0.github.io/oddjack-art/daily/">Daily Drops</a><a href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Redbubble</a><a href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a></nav></div></header>"""

for d in DESIGNS:
    slug = d["slug"]
    page_url = f"{SITE}/daily/{slug}/"
    img_url = f"{SITE}/images/{d['webimg']}"
    short = esc(d["blurb"][:150] + "\u2026")
    ld_offer_url = d["rb"] or d["kofi"] or page_url
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(d["title"])} \u2014 Daily Drop | Odd-jack</title>
<meta name="description" content="{short}">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(d["title"])} \u2014 Daily Drop | Odd-jack">
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
  "description": {json.dumps(d["blurb"][:160] + "\u2026")},
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
<p class="crumb"><a href="{SITE}/">Home</a> \u203a <a href="{SITE}/daily/">Daily Drops</a> \u203a {esc(d["title"])}</p>
<div class="product">
<div><img src="{img_url}" alt="{esc(d["title"])}"></div>
<div>
<h1>{esc(d["title"])}</h1>
<p class="price">$2.00 <span class="sub">USD \u00b7 fixed price</span></p>
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
