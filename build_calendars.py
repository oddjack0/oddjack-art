#!/usr/bin/env python3
"""Generate 4 calendar hub pages for oddjack-art (2027 wall calendars)."""
import os, html

BASE_URL = "https://oddjack0.github.io/oddjack-art/"
SITE = os.path.dirname(os.path.abspath(__file__))
KCAL = "/home/hatch/workspace/goals/multiply-income-streams/kofi-calendars"
IMGDIR = os.path.join(SITE, "images")

CALENDARS = [
    {"slug": "grumpy-cats-2027", "title": "Grumpy Cats 2027 Wall Calendar",
     "kofi": "https://ko-fi.com/s/7d30988a69",
     "blurb": "Twelve months of gloriously grumpy cats — deadpan, unimpressed, and judging your life choices all year long.",
     "tags": "2027 calendar, wall calendar, printable calendar, cat calendar, grumpy cat, funny cat calendar, monthly planner, digital download"},
    {"slug": "gothmas-cats-2027", "title": "Gothmas Cats 2027 Wall Calendar",
     "kofi": "https://ko-fi.com/s/aebd55308f",
     "blurb": "Dark-cozy Christmas cats in black, deep red, purple and silver — gothic holiday vibes for every month of 2027.",
     "tags": "2027 calendar, wall calendar, printable calendar, christmas cat calendar, goth christmas, gothmas, monthly planner, digital download"},
    {"slug": "cute-animals-2027", "title": "Cute Animals 2027 Wall Calendar",
     "kofi": "https://ko-fi.com/s/3fa8994c69",
     "blurb": "Twelve months of kawaii cute animals in soft pastels — bunnies, chicks, beach pups and snowy friends.",
     "tags": "2027 calendar, wall calendar, printable calendar, cute animals, kawaii calendar, monthly planner, digital download"},
    {"slug": "dogs-2027", "title": "Dogs 2027 Wall Calendar",
     "kofi": "https://ko-fi.com/s/ce961ba7b0",
     "blurb": "A whole year of funny, wholesome dogs — every breed bringing its own brand of chaos to each month.",
     "tags": "2027 calendar, wall calendar, printable calendar, dog calendar, puppy calendar, monthly planner, digital download"},
]

MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
MONTH_FILES = ["01-january.png", "02-february.png", "03-march.png", "04-april.png",
               "05-may.png", "06-june.png", "07-july.png", "08-august.png",
               "09-september.png", "10-october.png", "11-november.png", "12-december.png"]

CSS = """*{box-sizing:border-box}body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;margin:0;color:#2b2118;background:#fff8f1;line-height:1.6}
header{background:#1d1030;color:#fff;padding:.9rem 1rem}header .wrap{display:flex;justify-content:space-between;align-items:center;max-width:1100px;margin:0 auto}
.logo{color:#ffb347;font-weight:800;font-size:1.25rem;text-decoration:none}nav a{color:#fff;margin-left:1rem;text-decoration:none;font-size:.95rem}nav a:hover{text-decoration:underline}
.wrap{max-width:1100px;margin:0 auto;padding:0 1rem}.hero{background:linear-gradient(135deg,#1d1030,#5b2a86);color:#fff;padding:3rem 1rem;text-align:center}
.hero h1{font-size:2rem;margin:0 0 .5rem}.hero p{max-width:640px;margin:0 auto 1.2rem;color:#f3e8ff}
.btn{display:inline-block;background:#ff6b35;color:#fff;font-weight:700;padding:.7rem 1.4rem;border-radius:8px;text-decoration:none;margin:.25rem}
.btn:hover{background:#e55a28}.btn.alt{background:transparent;border:2px solid #fff}
h2{margin-top:2.2rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1rem;margin:1rem 0 2rem}
.card{background:#fff;border:1px solid #eee;border-radius:10px;overflow:hidden;text-decoration:none;color:inherit}
.card img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}.card .t{padding:.5rem .6rem;font-size:.85rem;font-weight:600}
.product{display:grid;grid-template-columns:1fr;gap:1.5rem;margin:1.5rem 0}@media(min-width:760px){.product{grid-template-columns:minmax(0,5fr) minmax(0,6fr)}}
.product img{width:100%;border-radius:12px}.price{font-size:1.6rem;font-weight:800;color:#ff6b35}
ul.tick{list-style:none;padding:0}ul.tick li::before{content:"\\2713 ";color:#2e9e5b;font-weight:700}
footer{background:#1d1030;color:#cbbde0;padding:2rem 1rem;margin-top:3rem;font-size:.9rem}footer a{color:#ffb347}"""

NAV = (f'<header><div class="wrap"><a class="logo" href="{BASE_URL}">🎃 Odd-jack Art</a><nav>'
       f'<a href="{BASE_URL}halloween/">Halloween</a><a href="{BASE_URL}cat-wallpapers/">Wallpapers</a>'
       f'<a href="{BASE_URL}printable-wall-art/">Prints</a><a href="{BASE_URL}niches/">Niches</a>'
       f'<a href="{BASE_URL}daily/">Daily Drops</a><a href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a>'
       f'</nav></div></header>')
FOOTER = (f'<footer><div class="wrap"><p><strong>Odd-jack Art</strong> — cute kawaii cats, elemental kitties, '
          f'psychedelic art &amp; spooky Halloween drops by Odd Jack O.M.T. Instant-download phone wallpapers, printable wall art &amp; sticker packs.</p>'
          f'<p><a href="https://ko-fi.com/oddjack/shop" rel="noopener">Shop all designs on Ko-fi</a> · '
          f'<a href="{BASE_URL}sitemap.xml">Sitemap</a></p><p>© 2026 Odd-jack. All art is original. Personal use only.</p></div></footer>')

def esc(s): return html.escape(s, quote=True)

def build_calendar_page(cal):
    theme = cal["slug"].replace("-2027", "")
    page_dir = os.path.join(SITE, "calendars", cal["slug"])
    os.makedirs(page_dir, exist_ok=True)
    url = f"{BASE_URL}calendars/{cal['slug']}/"
    # web images: cover 1200px + 12 month thumbs 700px
    from PIL import Image
    cover_src = f"{KCAL}/listing-assets/{theme}-cover.png"
    cover_web = f"calendar-{theme}-cover.jpg"
    Image.open(cover_src).convert("RGB").resize((1200, 1200), Image.LANCZOS).save(
        os.path.join(IMGDIR, cover_web), quality=82)
    month_imgs = []
    for mf, mname in zip(MONTH_FILES, MONTHS):
        web = f"calendar-{theme}-{mname}.jpg"
        Image.open(f"{KCAL}/masters/{theme}/{mf}").convert("RGB").resize((700, 700), Image.LANCZOS).save(
            os.path.join(IMGDIR, web), quality=78)
        month_imgs.append((web, mname.capitalize()))
    cards = "".join(
        f'<div class="card"><img src="{BASE_URL}images/{w}" alt="{esc(cal["title"])} — {m}" loading="lazy">'
        f'<div class="t">{m} 2027</div></div>' for w, m in month_imgs)
    body = f"""<main class="wrap">
<p style="font-size:.85rem"><a href="{BASE_URL}">Home</a> › <a href="{BASE_URL}calendars/">2027 Calendars</a> › {esc(cal['title'])}</p>
<div class="product">
<div><img src="{BASE_URL}images/{cover_web}" alt="{esc(cal['title'])}"></div>
<div>
<h1>{esc(cal['title'])}</h1>
<p class="price">$8.00 <span style="font-size:.9rem;color:#666;font-weight:400">USD · fixed price</span></p>
<p><a class="btn" href="{cal['kofi']}" rel="noopener">Get it on Ko-fi — $8</a></p>
<ul class="tick"><li>25 pages at 300 DPI — 12 full-page illustrations + 12 monthly date grids</li><li>12×12 inch wall calendar format, US holidays marked</li><li>Instant PDF download on Ko-fi</li><li>Original art by Odd Jack O.M.T. — personal use only</li></ul>
<p>{esc(cal['blurb'])} Print at home or at a print shop and hang the whole year.</p>
<p style="font-size:.85rem;color:#666">Tags: {esc(cal['tags'])}</p>
</div>
</div>
<h2>All 12 months</h2>
<div class="grid">{cards}</div>
</main>"""
    schema = ("<script type=\"application/ld+json\">{\"@context\":\"https://schema.org\",\"@type\":\"Product\","
              f"\"name\":{json_str(cal['title'])},\"image\":\"{BASE_URL}images/{cover_web}\","
              f"\"description\":{json_str(cal['blurb'])},\"brand\":{{\"@type\":\"Brand\",\"name\":\"Odd-jack\"}},"
              f"\"offers\":{{\"@type\":\"Offer\",\"priceCurrency\":\"USD\",\"price\":\"8\","
              f"\"availability\":\"https://schema.org/InStock\",\"url\":\"{cal['kofi']}\"}}}}</script>")
    page = (f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<title>{esc(cal['title'])} — Printable 2027 Wall Calendar — $8 | Odd-jack</title>\n"
            f"<meta name=\"description\" content=\"{esc(cal['blurb'])} 25-page printable PDF, 300 DPI, instant download on Ko-fi.\">\n"
            f"<link rel=\"canonical\" href=\"{url}\">\n"
            f"<meta property=\"og:type\" content=\"website\">\n<meta property=\"og:title\" content=\"{esc(cal['title'])} | Odd-jack\">\n"
            f"<meta property=\"og:description\" content=\"{esc(cal['blurb'])}\">\n"
            f"<meta property=\"og:url\" content=\"{url}\">\n"
            f"<meta property=\"og:image\" content=\"{BASE_URL}images/{cover_web}\">\n"
            f"<style>{CSS}</style>\n{schema}</head>\n<body>\n{NAV}\n{body}{FOOTER}\n</body>\n</html>")
    open(os.path.join(page_dir, "index.html"), "w").write(page)
    print("page:", url)
    return url

def json_str(s):
    import json as j
    return j.dumps(s)

def build_hub(urls):
    hub_dir = os.path.join(SITE, "calendars")
    os.makedirs(hub_dir, exist_ok=True)
    cards = "".join(
        f'<a class="card" href="{u}"><img src="{BASE_URL}images/calendar-{c["slug"].replace("-2027","")}-cover.jpg" '
        f'alt="{esc(c["title"])}" loading="lazy"><div class="t">{esc(c["title"])}</div>'
        f'<div class="p">$8.00</div></a>' for c, u in zip(CALENDARS, urls))
    page = (f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<title>2027 Wall Calendars — Printable PDF Calendars | Odd-jack</title>\n"
            f"<meta name=\"description\" content=\"Printable 2027 wall calendars by Odd-jack: grumpy cats, gothmas cats, cute animals and dogs. 25-page PDFs, instant download.\">\n"
            f"<link rel=\"canonical\" href=\"{BASE_URL}calendars/\">\n<style>{CSS}\n"
            f".card .p{{padding:0 .6rem .6rem;color:#ff6b35;font-weight:700;font-size:.85rem}}</style></head>\n"
            f"<body>\n{NAV}\n<main class=\"wrap\">\n"
            f"<p style=\"font-size:.85rem\"><a href=\"{BASE_URL}\">Home</a> › 2027 Calendars</p>\n"
            f"<h1>2027 Wall Calendars</h1>\n"
            f"<p>Printable 12×12\" wall calendars — 25 pages each at 300 DPI, 12 full-page illustrations plus monthly date grids with US holidays. Instant PDF download on Ko-fi, $8 each.</p>\n"
            f"<div class=\"grid\">{cards}</div>\n</main>{FOOTER}\n</body>\n</html>")
    open(os.path.join(hub_dir, "index.html"), "w").write(page)
    print("hub:", f"{BASE_URL}calendars/")

if __name__ == "__main__":
    urls = [build_calendar_page(c) for c in CALENDARS]
    build_hub(urls)
