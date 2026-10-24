import os, sys
from playwright.sync_api import sync_playwright
url = "file:///" + os.path.abspath("index.html").replace("\\", "/")
sels = sys.argv[1:]
JS = "(sels) => sels.map(s => { const e = document.querySelector(s); if (!e) return s + ': none'; const b = e.getBoundingClientRect(); return s + ': ' + Math.round(b.top + scrollY) + '-' + Math.round(b.bottom + scrollY); }).join(' | ')"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900}); pg.goto(url, wait_until="networkidle")
    h = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h, 700): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(40)
    pg.wait_for_timeout(800)
    print(pg.evaluate(JS, sels))
    b.close()
