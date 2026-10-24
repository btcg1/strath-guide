"""Contact sheets of the photo-wall candidates, grouped by trip/location, for a composition and duplicate review."""
import json, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
picks = json.load(open("data/picks.json", encoding="utf-8"))
trips = json.load(open("data/trips.json", encoding="utf-8"))
folder_trip = {f: t["id"] for t in trips for f in t["folders"]}
used = {p["file"] for p in picks["prints"]}
cands = []
for key in picks["wall"] + [k for t in trips for k in picks["trips"][t["id"]]]:
    if key not in used and key not in cands:
        cands.append(key)
groups = {}
for k in cands:
    sheet = k.rsplit("_", 1)[0]
    g = "glasgow" if sheet.startswith("gla-") or sheet == "pollok-art" else folder_trip.get(sheet, "other")
    groups.setdefault(g, []).append(k)
os.makedirs(".taste-skill/album", exist_ok=True)
font = ImageFont.truetype("arial.ttf", 22)
index = {}
TW, TH = 300, 400
for g, keys in groups.items():
    cols = min(6, len(keys)); rows = (len(keys) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (TW + 8), rows * (TH + 8) + 40), "white"); d = ImageDraw.Draw(sh)
    d.text((8, 8), g, fill="black", font=font)
    for i, k in enumerate(keys):
        im = Image.open(os.path.join("_source", k + ".jpg")).convert("RGB"); im.thumbnail((TW, TH))
        x, y = (i % cols) * (TW + 8), 40 + (i // cols) * (TH + 8)
        sh.paste(im, (x, y)); d.rectangle([x, y, x + 34, y + 30], fill="black"); d.text((x + 6, y + 3), str(i), fill="yellow", font=font)
    sh.save(f".taste-skill/album/{g}.jpg", quality=75)
    index[g] = keys
json.dump(index, open(".taste-skill/album/index.json", "w"), indent=1)
print(len(cands), "candidates in", len(groups), "groups:", {g: len(v) for g, v in groups.items()})
