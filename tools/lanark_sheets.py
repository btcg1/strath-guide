"""Contact sheets of the New Lanark photos on Drive (copy of wales_sheets.py with another folder), for a composition review.
Writes .taste-skill/wales/<place>.jpg (numbered thumbnails), index.json (number -> original path) and flags
near-duplicates of photos already on the site (dHash against _source/)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = r"G:\My Drive\Exchange (Sep-Dec 2025)\Scotland\Ricoh"
PLACES = {"lanark": r"New Lanark 17.10\Lanark", "clyde": r"New Lanark 17.10\River Clyde"}
OUT = os.path.join(".taste-skill", "lanark"); os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)

def dhash(im, n=8):
    g = im.convert("L").resize((n + 1, n))
    px = list(g.getdata())
    return sum(1 << i for i in range(n * n) if px[(i // n) * (n + 1) + i % n] > px[(i // n) * (n + 1) + i % n + 1])

existing = {}
for f in os.listdir("_source"):
    if f.split("_")[0] in ("lanark", "newlanark"):
        existing[f[:-4]] = dhash(Image.open(os.path.join("_source", f)))

font = ImageFont.truetype("arial.ttf", 22)
index = {}
TW, TH = 300, 300
for slug, folder in PLACES.items():
    d = os.path.join(BASE, folder)
    files = sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg")))
    thumbs = []
    for n, f in enumerate(files):
        tp = os.path.join(OUT, "thumbs", f"{slug}_{n}.jpg")
        if os.path.exists(tp):
            im = Image.open(tp)
        else:
            im = Image.open(os.path.join(d, f)); im.draft("RGB", (im.width // 4, im.height // 4))
            im = ImageOps.exif_transpose(im).convert("RGB"); im.thumbnail((600, 600)); im.save(tp, quality=80)
        h = dhash(im)
        dup = [k for k, v in existing.items() if bin(h ^ v).count("1") <= 8]
        index[f"{slug}_{n}"] = {"path": os.path.join(d, f), "dup_of": dup}
        t = im.copy(); t.thumbnail((TW, TH)); thumbs.append((n, t, dup))
        if n % 20 == 0:
            print(slug, n, "/", len(files), flush=True)
    cols = 8; rows = (len(thumbs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (TW + 6), rows * (TH + 6) + 36), "white"); dr = ImageDraw.Draw(sh)
    dr.text((6, 6), folder, fill="black", font=font)
    for i, (n, t, dup) in enumerate(thumbs):
        x, y = (i % cols) * (TW + 6), 36 + (i // cols) * (TH + 6)
        sh.paste(t, (x + (TW - t.width) // 2, y + (TH - t.height) // 2))
        dr.rectangle([x, y, x + 44, y + 28], fill="red" if dup else "black"); dr.text((x + 5, y + 2), str(n), fill="yellow", font=font)
    sh.save(os.path.join(OUT, f"{slug}.jpg"), quality=78)
    print("sheet", slug, len(thumbs), flush=True)
json.dump(index, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=1)
print("done", len(index), "photos;", sum(1 for v in index.values() if v["dup_of"]), "already on the site")
