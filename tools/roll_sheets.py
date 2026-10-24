"""Contact sheets of EVERY Ricoh trip photo on Drive, one sheet per place folder, for a full composition audit.
Writes .taste-skill/roll/<slug>.jpg (numbered thumbnails; red number = already on the site), thumbs/, and index.json
(slug -> folder, and "<slug>_<n>" -> original path). Re-runnable: thumbnails are cached."""
import json, os, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = r"G:\My Drive\Exchange (Sep-Dec 2025)"
OUT = os.path.join(".taste-skill", "roll"); os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)

def slugify(rel):
    parts = [p for p in rel.replace("\\", "/").split("/") if p not in ("Scotland", "Northern Ireland", "England & Wales", "Ricoh")]
    s = "-".join(re.sub(r"[\d.\s-]+$", "", p) for p in parts)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

folders = []
for top in ("Scotland", "Northern Ireland", "England & Wales"):
    for d, _, fs in os.walk(os.path.join(BASE, top, "Ricoh")):
        jp = sorted(f for f in fs if f.lower().endswith((".jpg", ".jpeg")))
        if jp:
            folders.append((slugify(os.path.relpath(d, BASE)), d, jp))

def dhash(im, n=8):
    g = im.convert("L").resize((n + 1, n)); px = list(g.getdata())
    return sum(1 << i for i in range(n * n) if px[(i // n) * (n + 1) + i % n] > px[(i // n) * (n + 1) + i % n + 1])
site = {f[:-4]: dhash(Image.open(os.path.join("_source", f))) for f in os.listdir("_source")}

def thumb(job):
    slug, d, n, f = job
    tp = os.path.join(OUT, "thumbs", f"{slug}_{n}.jpg")
    if not os.path.exists(tp):
        im = Image.open(os.path.join(d, f)); im.draft("RGB", (im.width // 4, im.height // 4))
        im = ImageOps.exif_transpose(im).convert("RGB"); im.thumbnail((600, 600)); im.save(tp, quality=80)
    im = Image.open(tp)
    h = dhash(im)
    return slug, n, os.path.join(d, f), [k for k, v in site.items() if bin(h ^ v).count("1") <= 8]

jobs = [(slug, d, n, f) for slug, d, fs in folders for n, f in enumerate(fs)]
print(len(folders), "folders,", len(jobs), "photos", flush=True)
index = {"folders": {slug: os.path.relpath(d, BASE) for slug, d, _ in folders}, "photos": {}}
done = 0
with ThreadPoolExecutor(6) as ex:
    for slug, n, path, dup in ex.map(thumb, jobs):
        index["photos"][f"{slug}_{n}"] = {"path": path, "on_site": dup}
        done += 1
        if done % 200 == 0:
            print(done, "/", len(jobs), flush=True)

font = ImageFont.truetype("arial.ttf", 22); TW = TH = 300
for slug, d, fs in folders:
    cols = 8; rows = (len(fs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (TW + 6), rows * (TH + 6) + 36), "white"); dr = ImageDraw.Draw(sh)
    dr.text((6, 6), index["folders"][slug], fill="black", font=font)
    for n in range(len(fs)):
        t = Image.open(os.path.join(OUT, "thumbs", f"{slug}_{n}.jpg")); t.thumbnail((TW, TH))
        x, y = (n % cols) * (TW + 6), 36 + (n // cols) * (TH + 6)
        sh.paste(t, (x + (TW - t.width) // 2, y + (TH - t.height) // 2))
        dr.rectangle([x, y, x + 44, y + 28], fill="red" if index["photos"][f"{slug}_{n}"]["on_site"] else "black")
        dr.text((x + 5, y + 2), str(n), fill="yellow", font=font)
    sh.save(os.path.join(OUT, f"{slug}.jpg"), quality=76)
json.dump(index, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=1)
print("done:", {slug: len(fs) for slug, _, fs in folders}, flush=True)
