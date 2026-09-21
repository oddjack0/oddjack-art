#!/usr/bin/env python3
"""Build the Odd-jack SEO static site. Rebuild with: python3 build.py"""
import json, os, re, shutil, html, datetime

BASE_URL = "https://oddjack0.github.io/oddjack-art/"
SHOP_URL = "https://ko-fi.com/oddjack/shop"
SRC = os.path.expanduser("~/workspace/kofi-challenge")
OUT = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-09-17"

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
<header><div class="wrap"><a class="logo" href="{BASE_URL}">🎃 Odd-jack Art</a><nav><a href="{BASE_URL}halloween/">Halloween</a><a href="{BASE_URL}cat-wallpapers/">Wallpapers</a><a href="{BASE_URL}printable-wall-art/">Prints</a><a href="{SHOP_URL}" rel="noopener">Ko-fi Shop</a></nav></div></header>
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

# ---------------- build ----------------
ITEMS = load_manifests()

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def main():
    global ITEMS
    ITEMS = load_manifests()
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
