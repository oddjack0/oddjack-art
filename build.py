#!/usr/bin/env python3
"""Build the Odd-jack SEO static site. Rebuild with: python3 build.py"""
import json, os, re, shutil, html, datetime

BASE_URL = "https://oddjack0.github.io/oddjack-art/"
SHOP_URL = "https://ko-fi.com/oddjack/shop"
SRC = os.path.expanduser("~/workspace/kofi-challenge")
OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-09-21"

# ---------------- data ----------------
def load_manifests():
    items = []  # (num, slug, title, description, kofi_url)
    order = {}
    with open(f"{SRC}/halloween-drop/ig-queue/ORDER.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"(\d+)\s+(\S+)\s+\|\s*(.*)", line)
            if m:
                order[m.group(2)] = int(m.group(1))
    m1 = json.load(open(f"{SRC}/halloween-drop/kofi-manifest.json"))
    m3 = json.load(open(f"{SRC}/halloween-drop/kofi-manifest-3.json"))
    u3 = json.load(open(f"{SRC}/halloween-drop/kofi-urls-3.json"))
    # map pin-urls.md design name -> kofi url (drop 2, designs 1-20)
    name2url = {}
    with open(f"{SRC}/halloween-drop/pin-urls.md") as f:
        for line in f:
            m = re.match(r"\d+\.\s+(.+?)\s+—\s+https://www\.pinterest\.com/\S+\s+→\s+(https://ko-fi\.com/s/\S+)", line.strip())
            if m:
                name2url[m.group(1).strip()] = m.group(2).strip()
    title2url = {t.split(" — ")[0]: u for t, u in name2url.items()}
    for entry in m1 + m3:
        slug = entry["slug"]
        num = order.get(slug)
        if not num:
            print(f"WARN: no ORDER number for {slug}, skipping")
            continue
        short = entry["title"].split(" — ")[0]
        if num <= 20:
            url = title2url.get(short)
        else:
            url = u3.get(str(num))
        if not url:
            print(f"WARN: no Ko-fi URL for #{num} {slug}; using shop URL")
            url = SHOP_URL
        items.append({"num": num, "slug": slug, "title": entry["title"],
                      "description": entry["description"], "url": url,
                      "img": f"{slug}.jpg", "price": 3.5})
    items.sort(key=lambda x: x["num"])
    return items

PACKS = [
    {"slug": "elemental-kitties-wallpaper-pack", "title": "Elemental Kitties Phone Wallpaper Pack",
     "price": 7, "img": "elemental-kitties-wallpapers-cover.jpg",
     "src_img": f"{SRC}/listings/elemental-kitties-wallpapers-cover.jpg",
     "description": "Six original kawaii cat phone wallpapers, each channeling a force of nature: Fire, Water, Earth, Storm, Ice, and Shadow. 6 high-res wallpapers (1152x2048, fits most phones), instant ZIP download. Original art by Odd Jack O.M.T. Personal use only."},
    {"slug": "psychedelic-cat-printable-bundle", "title": "Psychedelic Cat Printable Art Bundle",
     "price": 9, "img": "psychedelic-cat-art-bundle-cover.jpg",
     "src_img": f"{SRC}/listings/psychedelic-cat-art-bundle-cover.jpg",
     "description": "Six mind-bending psychedelic cat prints — swirling colors, cosmic patterns, and trippy kitties ready for your walls. 6 high-res printable art files (1120x2240 JPG). Print at home or any print shop. Original art by Odd Jack O.M.T. Personal use only."},
    {"slug": "spooky-halloween-cats-pack", "title": "Spooky Halloween Cats 6-Pack",
     "price": 7, "img": "spooky-halloween-cats-cover.jpg",
     "src_img": f"{SRC}/listings/spooky-halloween-cats-cover.jpg",
     "description": "Six spooky-cute Halloween kitties: Pumpkin, Ghost, Witch, Vampire, Skeleton, and Candy Corn. Perfect October phone wallpapers or prints. 6 high-res files (1120x2240 JPG), instant ZIP download. Original art by Odd Jack O.M.T. Personal use only."},
    {"slug": "odd-jack-cat-sticker-pack", "title": "Odd-Jack Cat Sticker Pack",
     "price": 5, "img": "odd-jack-sticker-pack-cover.jpg",
     "src_img": f"{SRC}/listings/odd-jack-sticker-pack-cover.jpg",
     "description": "Six kawaii cat sticker designs: Dizzy, Pizza, Astronaut, Cactus, Mushroom, and Taco cats. 6 high-res square designs (1600x1600 JPG) — print on sticker paper at home or upload to any sticker printing service. Original art by Odd Jack O.M.T. Personal use only."},
]

# ---------------- helpers ----------------
def esc(s):
    return html.escape(s, quote=True)

def pfmt(p):
    return f"${p:.2f}"

def meta_desc(text):
    t = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= 155 else t[:152].rsplit(" ", 1)[0] + "…"

CSS = """*{box-sizing:border-box}body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:0;color:#2b2118;background:#fff8f1;line-height:1.6}
header{background:#1d1030;color:#fff;padding:.9rem 1rem}header .wrap{display:flex;justify-content:space-between;align-items:center;max-width:1100px;margin:0 auto}
.logo{color:#ffb347;font-weight:800;font-size:1.25rem;text-decoration:none}nav a{color:#fff;margin-left:1rem;text-decoration:none;font-size:.95rem}nav a:hover{text-decoration:underline}
.wrap{max-width:1100px;margin:0 auto;padding:0 1rem}.hero{background:linear-gradient(135deg,#1d1030,#5b2a86);color:#fff;padding:3rem 1rem;text-align:center}
.hero h1{font-size:2rem;margin:0 0 .5rem}.hero p{max-width:640px;margin:0 auto 1.2rem;color:#f3e8ff}
.btn{display:inline-block;background:#ff6b35;color:#fff;font-weight:700;padding:.7rem 1.4rem;border-radius:8px;text-decoration:none;margin:.25rem}
.btn:hover{background:#e55a28}.btn.alt{background:transparent;border:2px solid #fff}
h2{margin-top:2.2rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1rem;margin:1rem 0 2rem}
.card{background:#fff;border:1px solid #eee;border-radius:10px;overflow:hidden;text-decoration:none;color:inherit}
.card img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block}.card .t{padding:.5rem .6rem;font-size:.85rem;font-weight:600}
.card .p{padding:0 .6rem .6rem;color:#ff6b35;font-weight:700;font-size:.85rem}
.product{display:grid;grid-template-columns:1fr;gap:1.5rem;margin:1.5rem 0}@media(min-width:760px){.product{grid-template-columns:minmax(0,5fr) minmax(0,6fr)}}
.product img{width:100%;border-radius:12px}.price{font-size:1.6rem;font-weight:800;color:#ff6b35}
ul.tick{list-style:none;padding:0}ul.tick li::before{content:"✓ ";color:#2e9e5b;font-weight:700}
footer{background:#1d1030;color:#cbbde0;padding:2rem 1rem;margin-top:3rem;font-size:.9rem}footer a{color:#ffb347}
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin:1.5rem 0}
.catcard{background:#fff;border:1px solid #eee;border-radius:10px;padding:1.2rem;text-decoration:none;color:inherit}.catcard h3{margin:.3rem 0;color:#5b2a86}"""

def head(title, desc, path, img=None, extra=""):
    url = BASE_URL + path
    img_tag = f'\n<meta property="og:image" content="{esc(BASE_URL + "images/" + img)}">' if img else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">{img_tag}
<style>{CSS}</style>
{extra}</head>
<body>
<header><div class="wrap"><a class="logo" href="{BASE_URL}">🎃 Odd-jack Art</a><nav><a href="{BASE_URL}halloween/">Halloween</a><a href="{BASE_URL}cat-wallpapers/">Wallpapers</a><a href="{BASE_URL}printable-wall-art/">Prints</a><a href="{BASE_URL}niches/">Niches</a><a href="{SHOP_URL}" rel="noopener">Ko-fi Shop</a></nav></div></header>
"""

FOOTER = f"""<footer><div class="wrap">
<p><strong>Odd-jack Art</strong> — cute kawaii cats, elemental kitties, psychedelic art &amp; spooky Halloween drops by Odd Jack O.M.T. Instant-download phone wallpapers, printable wall art &amp; sticker packs.</p>
<p><a href="{SHOP_URL}" rel="noopener">Shop all designs on Ko-fi</a> · <a href="{BASE_URL}sitemap.xml">Sitemap</a></p>
<p>© 2026 Odd-jack. All art is original. Personal use only.</p>
</div></footer>
</body>
</html>"""

def card(item, page_dir):
    return (f'<a class="card" href="{BASE_URL}{page_dir}">'
            f'<img src="{BASE_URL}images/{item["img"]}" alt="{esc(item["title"])} digital download" loading="lazy">'
            f'<div class="t">{esc(item["title"])}</div><div class="p">{pfmt(item["price"])}</div></a>')

def jsonld(name, desc, img, price, kofi_url):
    data = {"@context": "https://schema.org", "@type": "Product", "name": name,
            "image": BASE_URL + "images/" + img, "description": meta_desc(desc),
            "brand": {"@type": "Brand", "name": "Odd-jack"},
            "offers": {"@type": "Offer", "priceCurrency": "USD", "price": str(price),
                       "availability": "https://schema.org/InStock", "url": kofi_url}}
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2) + "\n</script>"

# ---------------- pages ----------------
def product_page(item):
    pdir = f"designs/{item['num']:02d}-{item['slug']}/"
    img_url = BASE_URL + "images/" + item["img"]
    others = [x for x in ITEMS if x["num"] != item["num"]]
    rel = [others[(item["num"] - 1 + i) % len(others)] for i in (1, 2, 3, 4)]
    rel_html = "".join(card(r, f"designs/{r['num']:02d}-{r['slug']}/") for r in rel)
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › <a href="{BASE_URL}halloween/">Halloween Cat Art</a> › {esc(item['title'])}</p>
<div class="product">
<div><img src="{img_url}" alt="{esc(item['title'])} digital download"></div>
<div>
<h1>{esc(item['title'])}</h1>
<p class="price">{pfmt(item['price'])} <span style="font-size:.9rem;color:#666;font-weight:400">USD · instant download</span></p>
<p><a class="btn" href="{esc(item['url'])}" rel="noopener">Buy instant download on Ko-fi</a></p>
<ul class="tick"><li>High-resolution JPG, instant download</li><li>Perfect as a phone wallpaper or printable wall art</li><li>Original art by Odd Jack O.M.T.</li><li>Personal use only</li></ul>
<p>{esc(item['description'])}</p>
</div>
</div>
<h2>You may also like</h2>
<div class="grid">{rel_html}</div>
</main>"""
    ld = jsonld(item["title"], item["description"], item["img"], item["price"], item["url"])
    return head(f"{item['title']} — Odd-jack Art", meta_desc(item["description"]), pdir, item["img"], ld) + body + FOOTER

def pack_page(p):
    pdir = f"packs/{p['slug']}/"
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › {esc(p['title'])}</p>
<div class="product">
<div><img src="{BASE_URL}images/{p['img']}" alt="{esc(p['title'])} digital download"></div>
<div>
<h1>{esc(p['title'])}</h1>
<p class="price">{pfmt(p['price'])} <span style="font-size:.9rem;color:#666;font-weight:400">USD · instant download</span></p>
<p><a class="btn" href="{SHOP_URL}" rel="noopener">Buy on Ko-fi</a></p>
<ul class="tick"><li>Instant ZIP download</li><li>Original art by Odd Jack O.M.T.</li><li>Personal use only</li></ul>
<p>{esc(p['description'])}</p>
</div>
</div>
<h2>More Halloween cat art</h2>
<div class="grid">{"".join(card(r, f"designs/{r['num']:02d}-{r['slug']}/") for r in ITEMS[:8])}</div>
</main>"""
    ld = jsonld(p["title"], p["description"], p["img"], p["price"], SHOP_URL)
    return head(f"{p['title']} — Odd-jack Art", meta_desc(p["description"]), pdir, p["img"], ld) + body + FOOTER

def homepage():
    featured = [ITEMS[i - 1] for i in (2, 27, 25, 21, 70, 50, 45, 61)]
    feat = "".join(card(r, f"designs/{r['num']:02d}-{r['slug']}/") for r in featured)
    body = f"""<div class="hero"><div class="wrap">
<h1>Halloween Cat Art &amp; Kawaii Cat Wallpapers</h1>
<p>Adorable spooky kitties as instant-download phone wallpapers, printable wall art &amp; stickers. New Halloween designs weekly — just $3.50 each.</p>
<p><a class="btn" href="{SHOP_URL}" rel="noopener">Shop all 74 designs on Ko-fi</a> <a class="btn alt" href="{BASE_URL}halloween/">Browse Halloween cats</a></p>
</div></div>
<main class="wrap">
<h2>Featured Halloween kitties</h2>
<div class="grid">{feat}</div>
<h2>Shop by category</h2>
<div class="cats">
<a class="catcard" href="{BASE_URL}halloween/"><h3>🎃 Halloween Cat Art</h3><p>70 spooky-cute designs: ghosts, witches, pumpkins &amp; haunted everything.</p></a>
<a class="catcard" href="{BASE_URL}cat-wallpapers/"><h3>📱 Cat Wallpapers</h3><p>Vertical phone wallpapers starring kawaii kitties.</p></a>
<a class="catcard" href="{BASE_URL}printable-wall-art/"><h3>🖼️ Printable Wall Art</h3><p>High-res cat art ready to print, frame &amp; hang.</p></a>
<a class="catcard" href="{BASE_URL}sticker-art/"><h3>✨ Sticker Art</h3><p>Kawaii cat designs made for sticker printing.</p></a>
</div>
<h2>New: shop by niche</h2>
<div class="cats">
{niche_home_cards_html()}
<a class="catcard" href="{BASE_URL}niches/"><h3>🧭 All 12 collections</h3><p>Browse every niche — Halloween cats, apparel niches &amp; digital products.</p></a>
</div>
<h2>About Odd-jack</h2>
<p>Odd art by Odd Jack O.M.T. — cute kawaii cats, elemental kitties, psychedelic art &amp; spooky Halloween drops. Every design is an instant digital download: buy once on Ko-fi and use it as your phone wallpaper, print it for your walls, or turn it into stickers. New designs drop weekly.</p>
<h2>All 70 Halloween designs</h2>
<div class="grid">{"".join(card(r, f"designs/{r['num']:02d}-{r['slug']}/") for r in ITEMS)}</div>
</main>"""
    desc = "70+ cute Halloween cat art designs as $3.50 instant downloads — kawaii cat phone wallpapers, printable wall art & sticker packs by Odd-jack."
    return head("Halloween Cat Art & Kawaii Cat Wallpapers — Odd-jack Art", desc, "", ITEMS[0]["img"]) + body + FOOTER

def category_page(path, h1, title, desc, intro_paras, items):
    grid = "".join(card(r, f"designs/{r['num']:02d}-{r['slug']}/") for r in items)
    intro = "".join(f"<p>{p}</p>" for p in intro_paras)
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › {esc(h1)}</p>
<h1>{esc(h1)}</h1>
{intro}
<div class="grid">{grid}</div>
<p><a class="btn" href="{SHOP_URL}" rel="noopener">Shop all designs on Ko-fi</a></p>
</main>"""
    return head(title, desc, path, items[0]["img"] if items else None) + body + FOOTER

# ---------------- niche expansion ----------------
RB_SHOP = "https://www.redbubble.com/people/Odd-jack/shop"
KOFI_HOME = "https://ko-fi.com/oddjack"
EXP_SRC = os.path.expanduser("~/workspace/goals/multiply-income-streams/niche-expansion/designs")
MAX_WEB_PX = 1400  # longest side for web images

NICHES = [
    {"folder": "rb-trades-pride", "slug": "trades-pride", "name": "Blue-Collar Trades Pride",
     "emoji": "🔧", "shop": "redbubble",
     "tagline": "Vintage badge graphics for the trades: diesel techs, welders, electricians, linemen & plumbers.",
     "seo": "Blue-collar trades pride apparel: diesel mechanic, welder, electrician, lineman & plumber badge tees, hoodies & stickers by Odd-jack.",
     "intros": ["Grease under the nails, pride on the chest. This collection turns each trade into a vintage badge graphic — crossed pistons for diesel techs, gear-and-spark emblems for welders, high-voltage attitude for electricians and linemen, and flow-state pride for plumbers.",
                "These designs are headed to the Odd-jack Redbubble shop as tees, hoodies, and hard-hat-ready stickers. Browse the full badge set below — new trades are dropping soon."]},
    {"folder": "rb-faith-apparel", "slug": "faith-apparel", "name": "Christian / Faith Apparel",
     "emoji": "✝️", "shop": "redbubble",
     "tagline": "Bold faith graphics — streetwear, varsity & boutique styles with crosses, sunsets & scripture vibes.",
     "seo": "Christian faith apparel: bold streetwear crosses, varsity faith tees & minimalist boutique designs by Odd-jack.",
     "intros": ["Wear your faith loud or keep it minimal — this collection covers both. Gritty streetwear graphics with glowing crosses and collegiate lettering, plus clean boutique pieces with mountain silhouettes and sunrise olive branches.",
                "These designs are headed to the Odd-jack Redbubble shop as tees and hoodies. Browse the styles below and find the one that speaks to your walk."]},
    {"folder": "rb-fishing-humor", "slug": "fishing-humor", "name": "Bass Fishing / Angler Humor",
     "emoji": "🎣", "shop": "redbubble",
     "tagline": "Sarcastic angler humor tees & decals for bass fishermen and their long-suffering families.",
     "seo": "Funny bass fishing shirts & angler humor decals: grumpy bass badges, retro dad fishing tees & pun graphics by Odd-jack.",
     "intros": ["Cranky by nature, born to fish. This collection is for the angler who fishes best before coffee — grumpy bass badges, retro 70s dad-fishing sunsets, night-bite moonlit scenes, and puns that belong on a boat ramp.",
                "These designs are headed to the Odd-jack Redbubble shop as tees, hoodies, and stickers. Perfect gifts for the fisherman in your life (or yourself)."]},
    {"folder": "rb-bookish-identity", "slug": "bookish", "name": "Bookish / BookTok Reader Identity",
     "emoji": "📚", "shop": "redbubble",
     "tagline": "Reader-identity tees for the TBR-pile guilty, romantasy girlies & smutty book clubs.",
     "seo": "Bookish reader tees: TBR pile humor, romantasy dragon art & smutty book club shirts for BookTok readers by Odd-jack.",
     "intros": ["One more chapter — that's the whole personality. This collection is reader-identity apparel for BookTok: towering TBR piles, gothic romantasy dragons, 2AM library clocks, and varsity-lettered book club eras.",
                "These designs are headed to the Odd-jack Redbubble shop as tees, hoodies, and laptop stickers. Your next book-club uniform is below."]},
    {"folder": "rb-america-250", "slug": "america-250", "name": "America 250th / Patriotic",
     "emoji": "🇺🇸", "shop": "redbubble",
     "tagline": "1776–2026 semiquincentennial badges: eagles, flags & liberty bells in cracked-ink vintage.",
     "seo": "America 250th patriotic apparel: 1776-2026 eagle, flag & liberty bell vintage badges for the semiquincentennial by Odd-jack.",
     "intros": ["250 years of freedom, 1776–2026. This collection marks America's semiquincentennial with cracked-ink heritage badges — bold eagles over worn flags, the Liberty Bell, and WE THE PEOPLE in constitutional lettering.",
                "These designs are headed to the Odd-jack Redbubble shop as tees, hoodies, and stickers. Proud statement pieces for the 4th of July, Veterans Day, and year-round patriotism."]},
    {"folder": "kf-planner-bundles", "slug": "planner-bundles", "name": "Printable Planner Bundles",
     "emoji": "🗓️", "shop": "kofi",
     "tagline": "Printable planners: ADHD focus, fitness, wedding, reading journals & creator finance.",
     "seo": "Printable planner bundles: ADHD focus planner, fitness & wellness, wedding planner, reading journal & creator finance by Odd-jack.",
     "intros": ["Print once, use forever. This collection of printable planner bundles is built for real life — ADHD-friendly daily focus spreads with time-blocking and dopamine menus, fitness and wellness logs, a full wedding planning system, a cozy reading journal, and a finance bundle for content creators.",
                "These bundles are headed to the Odd-jack Ko-fi shop as instant-download printable PDFs (US Letter & A4). Preview the covers and sample pages below."]},
    {"folder": "kf-canva-kits", "slug": "canva-kits", "name": "Canva Social-Media Template Kits",
     "emoji": "🎨", "shop": "kofi",
     "tagline": "Plug-and-play social templates: Pinterest growth kits, reel covers, carousels & brand kits.",
     "seo": "Canva social media template kits: Pinterest growth kits, reel covers, quote carousels, story engagement & small-biz brand kits by Odd-jack.",
     "intros": ["Stop designing from a blank page. These social-media template kits give creators scroll-stopping starting points — dark-academia Pinterest pin templates, viral-style reel covers, elegant quote carousels, story engagement stickers, and a full small-biz brand kit with logos, colors, and type.",
                "These kits are headed to the Odd-jack Ko-fi shop as instant downloads. Preview the kit covers and sample templates below."]},
    {"folder": "kf-notion-systems", "slug": "notion-systems", "name": "Notion Productivity Systems",
     "emoji": "🧠", "shop": "kofi",
     "tagline": "Notion dashboards & templates for creators, freelancers, students & goal-getters.",
     "seo": "Notion productivity templates: creator content OS, freelancer finance HQ, habit & goal tracker, project command & student second-brain by Odd-jack.",
     "intros": ["One calm dashboard for everything. These Notion productivity systems turn scattered docs into operating systems — a creator content pipeline, a freelancer money dashboard, a habit and goal tracker, a project command center, and a study dashboard for students.",
                "These systems are headed to the Odd-jack Ko-fi shop as instant-download Notion templates. Preview the dashboard mockups below."]},
]


def cover_for(idir, slug, m):
    """Find the cover image for an item, handling both metadata schemas:
    rb-style dict variants (variants[0]["file"]) and kf-style string variants
    (cover file is <slug>-cover.png)."""
    variants = m.get("variants") or []
    if variants and isinstance(variants[0], dict) and variants[0].get("file"):
        cand = os.path.join(idir, variants[0]["file"])
        if os.path.isfile(cand):
            return cand
    exact = os.path.join(idir, f"{slug}-cover.png")
    if os.path.isfile(exact):
        return exact
    for f in sorted(os.listdir(idir)):
        if f.endswith(("-cover.png", "-cover.jpg")) and os.path.isfile(os.path.join(idir, f)):
            return os.path.join(idir, f)
    return None


def load_expansion():
    items = []
    for n in NICHES:
        ndir = os.path.join(EXP_SRC, n["folder"])
        if not os.path.isdir(ndir):
            print(f"WARN: niche folder missing: {ndir}")
            continue
        for slug in sorted(os.listdir(ndir)):
            idir = os.path.join(ndir, slug)
            mf = os.path.join(idir, "metadata.json")
            if not os.path.isfile(mf):
                continue
            m = json.load(open(mf))
            cover_src = cover_for(idir, slug, m)
            if not cover_src:
                print(f"WARN: cover missing for {slug}")
                continue
            items.append({"niche": n, "slug": slug, "title": m["title"],
                          "description": m["description"], "tags": m.get("tags", []),
                          "price": m.get("price"), "cover_src": cover_src,
                          "format": m.get("format"), "page_count": m.get("page_count"),
                          "template_count": m.get("template_count"),
                          "resolution": m.get("resolution"), "note": m.get("note"),
                          "img": None})
    return items


def web_copy_image(item):
    """Resize master/cover to a web-sane JPEG copy in OUT/images. Masters untouched.
    Transparent artwork is composited onto white (site background is white anyway)."""
    from PIL import Image
    dest_name = f"niche-{item['niche']['slug']}-{item['slug']}-web.jpg"
    dest = os.path.join(OUT, "images", dest_name)
    if os.path.isfile(dest) and os.path.getmtime(dest) >= os.path.getmtime(item["cover_src"]):
        item["img"] = dest_name
        return dest_name
    im = Image.open(item["cover_src"])
    if max(im.size) > MAX_WEB_PX:
        im = im.resize((int(im.width * MAX_WEB_PX / max(im.size)),
                        int(im.height * MAX_WEB_PX / max(im.size))), Image.LANCZOS)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")
    im.save(dest, "JPEG", quality=82, optimize=True)
    item["img"] = dest_name
    return dest_name


def niche_card(item):
    pdir = f"niches/{item['niche']['slug']}/{item['slug']}/"
    price_html = pfmt(item["price"]) if item["price"] else "Coming soon"
    return (f'<a class="card" href="{BASE_URL}{pdir}">'
            f'<img src="{BASE_URL}images/{item["img"]}" alt="{esc(item["title"])}" loading="lazy">'
            f'<div class="t">{esc(item["title"])}</div><div class="p">{price_html}</div></a>')


def expansion_product_page(item, all_items):
    n = item["niche"]
    pdir = f"niches/{n['slug']}/{item['slug']}/"
    is_rb = n["shop"] == "redbubble"
    shop_url = RB_SHOP if is_rb else KOFI_HOME
    shop_name = "Redbubble" if is_rb else "Ko-fi"
    btn_label = "Browse the Redbubble shop" if is_rb else "Browse the Ko-fi shop"
    listed = item["price"] is not None
    price_html = (f'<p class="price">{pfmt(item["price"])} <span style="font-size:.9rem;color:#666;font-weight:400">USD · instant download</span></p>'
                  if listed else '<p class="price">Coming soon</p>')
    soon_html = (f'<p style="font-size:.9rem;color:#666">🚧 Coming soon to the shop — this design isn\'t listed yet. Follow the {shop_name} shop so you don\'t miss the drop.</p>'
                 if not listed else "")
    specs = [b for b in (item.get("format"),
                         f"{item['page_count']} pages" if item.get("page_count") else None,
                         f"{item['template_count']} templates" if item.get("template_count") else None,
                         item.get("resolution")) if b]
    specs_html = (f'<p style="font-size:.9rem;color:#555">Includes: {esc(" · ".join(specs))}</p>'
                  if listed and specs else "")
    note_html = (f'<p style="font-size:.9rem;color:#555">{esc(item["note"])}</p>'
                 if listed and item.get("note") else "")
    if is_rb:
        ticks = ["Original apparel-ready graphic by Odd Jack O.M.T.",
                 "Look for it on tees, hoodies & stickers",
                 "New drops land regularly — follow the shop"]
    elif listed:
        ticks = ["Instant digital download on Ko-fi",
                 "Original art & templates by Odd Jack O.M.T.",
                 "Personal use only"]
    else:
        ticks = ["Instant digital download on release",
                 "Original art & templates by Odd Jack O.M.T.",
                 "New drops land regularly — follow the shop"]
    tick_html = "".join(f"<li>{t}</li>" for t in ticks)
    tags_html = (f'<p style="font-size:.85rem;color:#666">Tags: {esc(", ".join(item["tags"][:12]))}</p>'
                 if item["tags"] else "")
    same = [x for x in all_items if x["niche"] == n and x is not item][:4]
    rel_html = "".join(niche_card(r) for r in same)
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › <a href="{BASE_URL}niches/">Shop by Niche</a> › <a href="{BASE_URL}niches/{n['slug']}/">{esc(n['name'])}</a> › {esc(item['title'])}</p>
<div class="product">
<div><img src="{BASE_URL}images/{item['img']}" alt="{esc(item['title'])}"></div>
<div>
<h1>{esc(item['title'])}</h1>
{price_html}
<p><a class="btn" href="{esc(shop_url)}" rel="noopener">{btn_label}</a></p>
{soon_html}
{specs_html}
{note_html}
<ul class="tick">{tick_html}</ul>
<p>{esc(item['description'])}</p>
{tags_html}
</div>
</div>
<h2>More in {esc(n['name'])}</h2>
<div class="grid">{rel_html}</div>
</main>"""
    ld_data = {"@context": "https://schema.org", "@type": "Product", "name": item["title"],
               "image": BASE_URL + "images/" + item["img"],
               "description": meta_desc(item["description"]),
               "brand": {"@type": "Brand", "name": "Odd-jack"}}
    if item["price"]:
        ld_data["offers"] = {"@type": "Offer", "priceCurrency": "USD", "price": str(item["price"]),
                             "availability": "https://schema.org/InStock", "url": shop_url}
    ld = '<script type="application/ld+json">\n' + json.dumps(ld_data, indent=2) + "\n</script>"
    return head(f"{item['title']} — {n['name']} | Odd-jack", meta_desc(item["description"]),
                pdir, item["img"], ld) + body + FOOTER


def niche_landing_page(n, items):
    pdir = f"niches/{n['slug']}/"
    grid = "".join(niche_card(it) for it in items)
    intro = "".join(f"<p>{p}</p>" for p in n["intros"])
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › <a href="{BASE_URL}niches/">Shop by Niche</a> › {esc(n['name'])}</p>
<h1>{n['emoji']} {esc(n['name'])}</h1>
{intro}
<div class="grid">{grid}</div>
<p><a class="btn" href="{RB_SHOP if n['shop'] == 'redbubble' else KOFI_HOME}" rel="noopener">Browse the shop</a> <a class="btn alt" style="color:#5b2a86;border-color:#5b2a86" href="{BASE_URL}niches/">All niches</a></p>
</main>"""
    return head(f"{n['name']} — {n['tagline']} | Odd-jack", n["seo"], pdir,
                items[0]["img"] if items else None) + body + FOOTER


def niche_count_line(n):
    items = [i for i in EXP_ITEMS if i["niche"] is n]
    count = len(items)
    priced = sum(1 for i in items if i["price"])
    if count and priced == count:
        return f"{count} designs"
    if priced:
        return f"{count} designs · more coming soon"
    return f"{count} designs · coming soon"


def niches_hub_page():
    existing = [
        ("halloween/", "🎃", "Halloween Cats", "70 spooky-cute kitty designs as $3.50 instant downloads.", "70 designs"),
        ("cat-wallpapers/", "📱", "Wallpapers", "Vertical kawaii cat phone wallpapers.", "70 designs"),
        ("printable-wall-art/", "🖼️", "Prints", "High-res cat art ready to print & frame.", "70 designs"),
        ("sticker-art/", "✨", "Sticker Packs", "Kawaii cat designs made for sticker printing.", "70+ designs"),
    ]
    cards = []
    for n in NICHES:
        count = niche_count_line(n)
        cards.append(f'<a class="catcard" href="{BASE_URL}niches/{n["slug"]}/"><h3>{n["emoji"]} {esc(n["name"])}</h3>'
                     f'<p>{esc(n["tagline"])}</p><p style="font-size:.8rem;color:#ff6b35;font-weight:700">{count}</p></a>')
    for path, emoji, name, tag, count in existing:
        cards.append(f'<a class="catcard" href="{BASE_URL}{path}"><h3>{emoji} {esc(name)}</h3>'
                     f'<p>{esc(tag)}</p><p style="font-size:.8rem;color:#ff6b35;font-weight:700">{count}</p></a>')
    body = f"""<div class="hero"><div class="wrap">
<h1>Shop by Niche</h1>
<p>Every Odd-jack collection in one place — spooky Halloween cats, blue-collar pride, faith apparel, angler humor, bookish tees, patriotic badges &amp; digital downloads.</p>
</div></div>
<main class="wrap">
<div class="cats">{"".join(cards)}</div>
</main>"""
    desc = "Shop every Odd-jack collection by niche: Halloween cats, trades pride, faith apparel, fishing humor, bookish tees, America 250th, planners, templates & Notion systems."
    return head("Shop by Niche — All Odd-jack Collections", desc, "niches/",
                EXP_ITEMS[0]["img"] if EXP_ITEMS else None) + body + FOOTER


def niche_home_cards_html():
    cards = []
    for n in NICHES:
        count = niche_count_line(n)
        cards.append(f'<a class="catcard" href="{BASE_URL}niches/{n["slug"]}/"><h3>{n["emoji"]} {esc(n["name"])}</h3>'
                     f'<p>{esc(n["tagline"])}</p><p style="font-size:.8rem;color:#ff6b35;font-weight:700">{count}</p></a>')
    return "".join(cards)


def build_expansion(pages):
    """Write niche hub, niche landings, and item pages. Appends to pages list.
    Requires EXP_ITEMS loaded and web images copied (done in main())."""
    write("niches/index.html", niches_hub_page()); pages.append(("niches/", "0.9"))
    for n in NICHES:
        items = [i for i in EXP_ITEMS if i["niche"] is n]
        pdir = f"niches/{n['slug']}/"
        write(pdir + "index.html", niche_landing_page(n, items)); pages.append((pdir, "0.8"))
        for it in items:
            ipdir = f"niches/{n['slug']}/{it['slug']}/"
            write(ipdir + "index.html", expansion_product_page(it, EXP_ITEMS))
            pages.append((ipdir, "0.7"))
    print(f"Expansion: {len(EXP_ITEMS)} items across {len(NICHES)} niches")

EXP_ITEMS = []
# ---------------- build ----------------
ITEMS = load_manifests()

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def main():
    global ITEMS, EXP_ITEMS
    ITEMS = load_manifests()
    EXP_ITEMS = load_expansion()
    os.makedirs(f"{OUT}/images", exist_ok=True)
    # copy images
    missing = []
    for it in ITEMS:
        src = f"{SRC}/products/{it['img']}"
        if os.path.exists(src):
            shutil.copy2(src, f"{OUT}/images/{it['img']}")
        else:
            missing.append(it['img'])
    for p in PACKS:
        if os.path.exists(p["src_img"]):
            shutil.copy2(p["src_img"], f"{OUT}/images/{p['img']}")
        else:
            missing.append(p["img"])
    if missing:
        print("MISSING IMAGES:", missing)
    for it in EXP_ITEMS:
        web_copy_image(it)

    pages = []  # (path, priority)
    write("index.html", homepage()); pages.append(("", "1.0"))
    for it in ITEMS:
        pdir = f"designs/{it['num']:02d}-{it['slug']}/"
        write(pdir + "index.html", product_page(it)); pages.append((pdir, "0.8"))
    for p in PACKS:
        pdir = f"packs/{p['slug']}/"
        write(pdir + "index.html", pack_page(p)); pages.append((pdir, "0.7"))

    cats = [
        ("halloween/", "70 Halloween Cat Art Designs — Spooky Cute Kitties",
         "70 Halloween Cat Art Designs — Spooky Cute Kitties | Odd-jack",
         "Shop 70 spooky-cute Halloween cat art designs: ghost kitties, witch cats, pumpkin patch art & haunted Halloween wallpapers. $3.50 instant downloads.",
         ["Looking for the cutest Halloween cat art on the internet? You've found it. This collection packs 70 original spooky-cute kitty designs — from Ghost Ship Kitty sailing haunted seas to Pumpkin Spice Latte Kitty sipping fall's favorite drink.",
          "Every design is a $3.50 instant download on Ko-fi. Use them as Halloween phone wallpapers, print them as October wall art, or turn them into stickers for your laptop and water bottle. New Halloween drops land weekly, so check back often — or follow the Ko-fi shop to get notified."],
         ITEMS),
        ("cat-wallpapers/", "Kawaii Cat Phone Wallpapers — Cute Cat Backgrounds",
         "Kawaii Cat Phone Wallpapers — Cute Cat Backgrounds | Odd-jack",
         "Cute kawaii cat phone wallpapers: Halloween kitties, elemental cats & more. Vertical high-res backgrounds, $3.50 instant downloads.",
         ["Give your phone a glow-up with kawaii cat wallpapers. Every Odd-jack design is drawn in tall vertical format made for phone screens — Halloween kitties, elemental cats, and spooky-cute scenes that look sharp on any lock screen.",
          "Each wallpaper is a $3.50 instant download: buy once, keep forever, swap whenever the mood strikes. Looking for autumn vibes? Start with the Halloween collection below."],
         ITEMS),
        ("printable-wall-art/", "Printable Cat Wall Art — Cute Halloween Prints",
         "Printable Cat Wall Art — Cute Halloween Prints | Odd-jack",
         "Printable cute cat wall art: high-res Halloween kitty prints ready to download, print & frame. $3.50 instant downloads by Odd-jack.",
         ["Decorate for spooky season (or all year) with printable cat wall art. These high-resolution designs print beautifully at home or at any print shop — frame a single statement piece or build a whole gallery wall of kitties.",
          "Every print is a $3.50 instant download with personal-use rights. Browse the full Halloween collection below and find your new favorite wall."],
         ITEMS),
        ("sticker-art/", "Cute Cat Sticker Art — Kawaii Sticker Designs",
         "Cute Cat Sticker Art — Kawaii Sticker Designs | Odd-jack",
         "Kawaii cat sticker art: cute Halloween & everyday kitty designs made for sticker printing. $3.50 instant downloads.",
         ["Stickers make everything better, and these kawaii cat designs were born for it. Download any design and print it on sticker paper at home, or upload it to your favorite sticker printing service for pro-quality vinyl stickers.",
          "Laptops, water bottles, journals, phone cases — stick a spooky-cute kitty on all of it. Start with the dedicated sticker pack or pick any Halloween design below."],
         ITEMS),
    ]
    for path, h1, title, desc, paras, items in cats:
        write(path + "index.html", category_page(path, h1, title, desc, paras, items))
        pages.append((path, "0.9"))

    # niche expansion: hub, niche landings, item pages
    build_expansion(pages)

    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri in pages:
        sm.append(f"  <url><loc>{esc(BASE_URL + path)}</loc><lastmod>{TODAY}</lastmod>"
                  f"<changefreq>weekly</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")

    print(f"Built {len(pages)} pages + sitemap.xml + robots.txt")
    print(f"Images copied: {len(os.listdir(f'{OUT}/images'))}")

if __name__ == "__main__":
    main()
