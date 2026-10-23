#!/usr/bin/env python3
"""Build daily-drop hub pages for 2026-10-22 (was skipped by its run — debt) and
2026-10-23 (coming-soon blocks; re-run with live URLs after the publisher run).
Also generates 1920x1920 web JPGs in images/.
"""
import html, json, os
from PIL import Image

SITE = "https://oddjack0.github.io/oddjack-art"
OUT_BASE = "/home/hatch/workspace/oddjack-site/daily"
IMG_DIR = "/home/hatch/workspace/oddjack-site/images"
DES = "/home/hatch/workspace/redbubble/designs/daily"

DESIGNS = [
    # --- 2026-10-22 (RB + Ko-fi live; pages were never built) ---
    {
        "date": "2026-10-22",
        "slug": "2026-10-22-hibernation-is-my-rsvp-grumpy-bear-skips-thanksgiving",
        "title": "Hibernation Is My RSVP: Grumpy Bear Skips Thanksgiving",
        "src": f"{DES}/2026-10-22/1/hibernation-rsvp-bear.png",
        "blurb": "This bear chose the blanket fort over the family gathering, and honestly? Correct call. Deadpan hibernation energy with a side of pie.",
        "tags": "unimpressed bear art, deadpan holiday humor, blanket fort illustration, antisocial animal tee, cute brown bear, fall feast funny, pumpkin pie design, cozy den sticker, sarcastic introvert gift, flat cartoon animal, november gathering gag, sleepy wildlife humor, comfort nap design, funny mammal shirt, grump lifestyle art",
        "rb": "https://www.redbubble.com/shop/ap/184946928",
        "kofi": "https://ko-fi.com/s/33a0c91be4",
    },
    {
        "date": "2026-10-22",
        "slug": "2026-10-22-social-battery-at-0-grumpy-gamer-cat",
        "title": "Social Battery at 0%: Grumpy Gamer Cat",
        "src": f"{DES}/2026-10-22/2/social-battery-gamer-cat.png",
        "blurb": "Headset on, controller glowing, patience gone. This cat ran out of social battery three lobbies ago and he's not recharging for anyone.",
        "tags": "funny gaming tee, unimpressed cat illustration, deadpan gamer humor, sarcastic cat sticker, headset cat design, controller cat art, low battery joke, flat cartoon cat, gaming night gift, tired gamer aesthetic, introvert gamer tee, energy drink humor, cute grumpy animal, late night gaming, relatable gamer design",
        "rb": "https://www.redbubble.com/shop/ap/184947020",
        "kofi": "https://ko-fi.com/s/b5b7210322",
    },
    {
        "date": "2026-10-22",
        "slug": "2026-10-22-my-flop-era-grumpy-goldfish",
        "title": "My Flop Era: Grumpy Goldfish",
        "src": f"{DES}/2026-10-22/3/flop-era-goldfish.png",
        "blurb": "Crown's cracked, bowl's tiny, attitude's massive. This goldfish is officially in his flop era and taking no questions.",
        "tags": "unimpressed fish art, deadpan pet humor, sarcastic goldfish tee, tiny bowl design, crowned fish illustration, funny aquarium sticker, relatable flop joke, flat cartoon fish, cranky pet design, orange fish art, kawaii fish humor, pet lover gift, sassy animal shirt, underwater funny design, crown pet illustration",
        "rb": "https://www.redbubble.com/shop/ap/184947086",
        "kofi": "https://ko-fi.com/s/7a8e19e3a7",
    },
    # --- 2026-10-23 (live URLs filled in after the publisher run) ---
    {
        "date": "2026-10-23",
        "slug": "2026-10-23-sous-chef-of-sass-grumpy-cat-on-gravy-duty",
        "title": "Sous-Chef of Sass: Grumpy Cat on Gravy Duty",
        "src": f"{DES}/2026-10-23/1/design-1.png",
        "blurb": "A stern orange tabby in a chef's hat inspects the holiday gravy with a clipboard and a merciless side-eye. The deadpan Thanksgiving tee every kitchen control freak secretly is.",
        "tags": "grumpy chef cat, funny thanksgiving shirt, sarcastic cat, cat chef art, thanksgiving cat, gravy lover gift, deadpan humor, cute grumpy animal, thanksgiving humor, cat foodie, sticker art, fall harvest, orange tabby, funny cook gift, kawaii cat",
        "rb": None, "kofi": None,
    },
    {
        "date": "2026-10-23",
        "slug": "2026-10-23-stuffing-critic-grumpy-goose-at-the-family-table",
        "title": "Stuffing Critic: Grumpy Goose at the Family Table",
        "src": f"{DES}/2026-10-23/2/design-2.png",
        "blurb": "This goose brought reading glasses to dinner and holds a forkful of stuffing like evidence in a trial. For anyone who has sat at a family table being judged by a relative with standards.",
        "tags": "grumpy goose thanksgiving, funny thanksgiving shirt, sarcastic thanksgiving, goose art, thanksgiving humor, food critic gift, deadpan animal, family dinner humor, cute goose, turkey day, sticker design, fall animal, funny bird tee, holiday dinner gift, kawaii goose",
        "rb": None, "kofi": None,
    },
    {
        "date": "2026-10-23",
        "slug": "2026-10-23-nap-season-sleepy-harvest-owl-skips-the-pie",
        "title": "Nap Season: Sleepy Harvest Owl Skips the Pie",
        "src": f"{DES}/2026-10-23/3/design-3.png",
        "blurb": "A grumpy owl burrito-wrapped in a knit blanket chooses a steaming mug over the pumpkin pie on the table. Nap season is a lifestyle, and this deadpan fall tee gets it.",
        "tags": "grumpy fall owl, funny thanksgiving shirt, autumn owl art, sleepy owl, fall harvest, pumpkin pie lover, cozy fall, deadpan humor, cute owl, thanksgiving humor gift, sticker art, fall leaves, funny owl shirt, coffee owl, kawaii owl",
        "rb": None, "kofi": None,
    },
]

# Filled in from the publisher run results (edit before re-running the second time)
URLS = {
    "2026-10-23-sous-chef-of-sass-grumpy-cat-on-gravy-duty": {"rb": "https://www.redbubble.com/shop/ap/184979661", "kofi": "https://ko-fi.com/s/2dd03723de"},
    "2026-10-23-stuffing-critic-grumpy-goose-at-the-family-table": {"rb": "https://www.redbubble.com/shop/ap/184979714", "kofi": "https://ko-fi.com/s/dabb4799d7"},
    "2026-10-23-nap-season-sleepy-harvest-owl-skips-the-pie": {"rb": "https://www.redbubble.com/shop/ap/184979754", "kofi": "https://ko-fi.com/s/ccca637f43"},
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
    {"slug": "2026-10-21-gravy-guard-grumpy-cat-on-potato-patrol", "webimg": "daily-2026-10-21-gravy-guard-grumpy-cat-on-potato-patrol-web.jpg", "title": "Gravy Guard: Grumpy Cat on Potato Patrol"},
    {"slug": "2026-10-21-premium-snack-vault-pie-protecting-raccoon", "webimg": "daily-2026-10-21-premium-snack-vault-pie-protecting-raccoon-web.jpg", "title": "Premium Snack Vault: Pie-Protecting Raccoon"},
]

for d in DESIGNS:
    # web JPG
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
