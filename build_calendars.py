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

CSS = """*{box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;margin:0;color:#f0edff;background:#0b0b12;line-height:1.6}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;font-weight:700;letter-spacing:.01em;color:#fff}
a{color:#5ce1ff}
header{position:sticky;top:0;z-index:50;background:rgba(11,11,18,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid #23232f;padding:.85rem 1rem}
header .wrap{display:flex;justify-content:space-between;align-items:center;max-width:1120px;margin:0 auto;gap:.8rem;flex-wrap:wrap}
.logo{font-family:Georgia,"Times New Roman",serif;font-size:1.2rem;letter-spacing:4px;font-weight:700;text-decoration:none;background:linear-gradient(90deg,#ff3bd4,#7c5cff);-webkit-background-clip:text;background-clip:text;color:transparent;white-space:nowrap}
nav{display:flex;gap:1.1rem;align-items:center;flex-wrap:wrap}
nav a{color:#b9b4d6;text-decoration:none;font-size:.9rem}
nav a:hover{color:#fff}
.wrap{max-width:1120px;margin:0 auto;padding:0 1.25rem}
.hero{text-align:center;padding:4.5rem 1rem 3.5rem;background:radial-gradient(ellipse 65% 55% at 50% 0%,#1b1030 0%,#0b0b12 72%)}
.hero .kick{font-size:.75rem;letter-spacing:5px;color:#8f89b3;text-transform:uppercase;margin:0 0 .9rem;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.hero h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.05;margin:0 0 1rem}
.hero h1 .grad{background:linear-gradient(90deg,#ff3bd4,#ffb13d,#5ce1ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:#a9a4c6;max-width:640px;margin:0 auto 1.4rem}
.btn{display:inline-block;background:#22d3ee;border:1px solid #22d3ee;color:#06222a;font-weight:700;padding:.75rem 1.6rem;border-radius:999px;text-decoration:none;margin:.25rem;box-shadow:0 0 22px rgba(34,211,238,.45);transition:transform .15s ease,box-shadow .15s ease}
.btn:hover{transform:translateY(-2px);box-shadow:0 0 32px rgba(34,211,238,.65);color:#06222a}
.btn.alt{background:transparent;border:1px solid #ff3bd4;color:#ff8ade;box-shadow:0 0 14px rgba(255,59,212,.3)}
.btn.alt:hover{box-shadow:0 0 26px rgba(255,59,212,.55);color:#fff}
.btn.rb{background:#ff3bd4;border-color:#ff3bd4;color:#14060f;box-shadow:0 0 22px rgba(255,59,212,.45)}
.btn.rb:hover{box-shadow:0 0 32px rgba(255,59,212,.65);color:#14060f}
.btn.sm{padding:.5rem 1.1rem;font-size:.85rem}
.btns{display:flex;gap:.6rem;flex-wrap:wrap;margin:1rem 0}
h2{margin-top:2.4rem;font-size:1.65rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:1.1rem;margin:1rem 0 2.5rem}
.card{background:#14141d;border:1px solid #262633;border-radius:14px;overflow:hidden;text-decoration:none;color:#f0edff;display:flex;flex-direction:column;transition:transform .2s ease,border-color .2s ease}
a.card:hover{transform:translateY(-4px);border-color:#ff3bd4}
.card img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;background:#1d1d2b}
.card .t{padding:.7rem .8rem .25rem;font-size:.88rem;font-weight:600}
.card .p{padding:0 .8rem .85rem;color:#ff8ade;font-weight:700;font-size:.85rem}
.product{display:grid;grid-template-columns:1fr;gap:2rem;margin:2rem 0}
@media(min-width:760px){.product{grid-template-columns:minmax(0,5fr) minmax(0,6fr)}}
.product img{width:100%;border-radius:14px;border:1px solid #262633;box-shadow:0 0 44px rgba(124,92,255,.18);background:#1d1d2b}
.product h1{margin-top:0}
.price{font-size:1.7rem;font-weight:800;color:#fff;font-family:Georgia,"Times New Roman",serif}
.price .sub{font-size:.9rem;color:#8f89b3;font-weight:400;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
ul.tick{list-style:none;padding:0}
ul.tick li{padding:.28rem 0;color:#c9c4e4}
ul.tick li::before{content:"✓ ";color:#5ce1ff;font-weight:700}
.crumb{font-size:.85rem;color:#8f89b3}
.crumb a{color:#b9b4d6;text-decoration:none}
.crumb a:hover{color:#fff}
.note{font-size:.9rem;color:#a9a4c6;background:#14141d;border:1px solid #262633;border-radius:10px;padding:.7rem 1rem}
.tags{font-size:.85rem;color:#8f89b3}
.count{font-size:.8rem;color:#ff8ade;font-weight:700}
.missing{font-size:.85rem;color:#ff9d9d}
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1.1rem;margin:1.5rem 0}
.catcard{background:linear-gradient(135deg,#1b1030,#0f1c33);border:1px solid #33334d;border-radius:14px;padding:1.4rem;text-decoration:none;color:#f0edff;transition:transform .2s ease,border-color .2s ease}
.catcard:hover{transform:translateY(-4px);border-color:#7c5cff}
.catcard h3{margin:.3rem 0 .4rem;color:#fff;font-size:1.15rem}
.catcard p{color:#a9a4c6;font-size:.92rem;margin:.35rem 0}
.related-guides{margin:2rem 0;background:#14141d;border:1px solid #262633;border-radius:14px;padding:1.2rem 1.4rem}
.related-guides h2{margin-top:0;font-size:1.2rem}
.related-guides ul{margin:.4rem 0;padding-left:1.2rem}
.related-guides li{margin:.3rem 0;color:#c9c4e4}
footer{border-top:1px solid #23232f;margin-top:4rem;padding:2.5rem 1rem 0;font-size:.9rem;background:#0e0e16}
footer .fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem;max-width:1120px;margin:0 auto}
footer h4{font-size:.78rem;letter-spacing:2px;color:#8f89b3;text-transform:uppercase;margin:0 0 .8rem;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
footer p{color:#a9a4c6}
footer a{color:#c9c4e4;text-decoration:none}
footer a:hover{color:#fff}
footer .fgrid a{display:block;margin-bottom:.55rem;font-size:.9rem}
footer .fcta{display:flex;gap:.6rem;margin-top:1rem;flex-wrap:wrap}
footer .fcta a{display:inline-block;margin-bottom:0}
footer .copy{text-align:center;color:#5c5878;font-size:.8rem;margin:2rem 0 0;padding-bottom:1.5rem}
@media(max-width:700px){footer .fgrid{grid-template-columns:1fr}.grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}"""

NAV = (f'<header><div class="wrap"><a class="logo" href="{BASE_URL}">ODD-JACK ART</a><nav>'
       f'<a href="{BASE_URL}halloween/">Halloween</a><a href="{BASE_URL}cat-wallpapers/">Wallpapers</a>'
       f'<a href="{BASE_URL}printable-wall-art/">Prints</a><a href="{BASE_URL}niches/">Niches</a>'
       f'<a href="{BASE_URL}daily/">Daily Drops</a>'
       f'<a href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Redbubble</a>'
       f'<a href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a>'
       f'</nav></div></header>')
FOOTER = (f'<footer><div class="wrap"><div class="fgrid">'
          f'<div><h4>Odd-jack Art</h4><p>Cute kawaii cats, elemental kitties, '
          f'psychedelic art &amp; spooky Halloween drops by Odd Jack O.M.T. Instant-download phone wallpapers, printable wall art &amp; sticker packs.</p>'
          f'<div class="fcta"><a class="btn sm" href="https://ko-fi.com/oddjack/shop" rel="noopener">Ko-fi Shop</a>'
          f'<a class="btn alt sm" href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Redbubble</a></div></div>'
          f'<div><h4>Shop</h4><a href="https://ko-fi.com/oddjack/shop" rel="noopener">All designs on Ko-fi</a>'
          f'<a href="https://www.redbubble.com/people/Odd-jack/shop" rel="noopener">Merch on Redbubble</a>'
          f'<a href="{BASE_URL}bundles/">$16 Bundle Packs</a><a href="{BASE_URL}calendars/">2027 Wall Calendars</a></div>'
          f'<div><h4>Explore</h4><a href="{BASE_URL}niches/">Shop by Niche</a>'
          f'<a href="{BASE_URL}daily/">Daily Drops</a><a href="{BASE_URL}morbid-quotes/">Morbid Quotes</a>'
          f'<a href="{BASE_URL}sitemap.xml">Sitemap</a></div>'
          f'</div><p class="copy">© 2026 Odd-jack. All art is original. Personal use only.</p></div></footer>')

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
<p class="crumb"><a href="{BASE_URL}">Home</a> › <a href="{BASE_URL}calendars/">2027 Calendars</a> › {esc(cal['title'])}</p>
<div class="product">
<div><img src="{BASE_URL}images/{cover_web}" alt="{esc(cal['title'])}"></div>
<div>
<h1>{esc(cal['title'])}</h1>
<p class="price">$8.00 <span class="sub">USD · fixed price</span></p>
<p><a class="btn" href="{cal['kofi']}" rel="noopener">Get it on Ko-fi — $8</a></p>
<ul class="tick"><li>25 pages at 300 DPI — 12 full-page illustrations + 12 monthly date grids</li><li>12×12 inch wall calendar format, US holidays marked</li><li>Instant PDF download on Ko-fi</li><li>Original art by Odd Jack O.M.T. — personal use only</li></ul>
<p>{esc(cal['blurb'])} Print at home or at a print shop and hang the whole year.</p>
<p class="tags">Tags: {esc(cal['tags'])}</p>
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
            f"<link rel=\"canonical\" href=\"{BASE_URL}calendars/\">\n<style>{CSS}</style></head>\n"
            f"<body>\n{NAV}\n<main class=\"wrap\">\n"
            f"<p class=\"crumb\"><a href=\"{BASE_URL}\">Home</a> › 2027 Calendars</p>\n"
            f"<h1>2027 Wall Calendars</h1>\n"
            f"<p>Printable 12×12\" wall calendars — 25 pages each at 300 DPI, 12 full-page illustrations plus monthly date grids with US holidays. Instant PDF download on Ko-fi, $8 each.</p>\n"
            f"<div class=\"grid\">{cards}</div>\n</main>{FOOTER}\n</body>\n</html>")
    open(os.path.join(hub_dir, "index.html"), "w").write(page)
    print("hub:", f"{BASE_URL}calendars/")

if __name__ == "__main__":
    urls = [build_calendar_page(c) for c in CALENDARS]
    build_hub(urls)
