"""Full-page screenshots with every image loaded and every entrance finished, cut into 1400px slices for review."""
import os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".taste-skill", "shots")
os.makedirs(OUT, exist_ok=True)
tag = sys.argv[1] if len(sys.argv) > 1 else "r"
url = "file:///" + os.path.join(ROOT, "index.html").replace("\\", "/")
Image.MAX_IMAGE_PIXELS = None
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [("desk", 1440, 900), ("phone", 390, 844)]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(url, wait_until="networkidle")
        pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
        H = pg.evaluate("document.documentElement.scrollHeight")
        for y in range(0, H, 500):
            pg.evaluate(f"window.scrollTo(0, {y})"); pg.wait_for_timeout(40)
        pg.evaluate("document.querySelectorAll('[data-reveal]').forEach(e => e.classList.add('is-in'))")
        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(2500)
        full = os.path.join(OUT, f"{tag}-{name}-full.png")
        pg.screenshot(path=full, full_page=True)
        im = Image.open(full); W, HH = im.size
        n = 0
        for top in range(0, HH, 1400):
            im.crop((0, top, W, min(HH, top + 1400))).convert("RGB").save(os.path.join(OUT, f"{tag}-{name}-{n:02d}.jpg"), quality=72)
            n += 1
        os.remove(full)
        print(name, W, HH, n, "slices")
        pg.close()
    b.close()
