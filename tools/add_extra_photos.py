"""Vendor the Codex-picked New Lanark and Chester/North Wales photos from Drive into _source/ (resized, no EXIF),
add the mill photos to the New Lanark album group, and build data/extra.json for an extra Chester & North Wales section.
One-time; picks from .taste-skill review on 2026-10-25."""
import json, os
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANARK = {"lanark": [5, 8, 20, 41, 46], "clyde": [12, 18, 30]}
WALES = {"chester": [10, 20, 26, 38, 43, 58, 82], "conwy": [11, 18, 26, 40, 65, 75], "snowdonia": [9, 23, 33, 51, 62, 75],
         "shrewsbury": [8, 16, 35, 54, 59], "manchester": [4, 24, 30, 36]}
idx = {**json.load(open(".taste-skill/lanark/index.json", encoding="utf-8")), **json.load(open(".taste-skill/wales/index.json", encoding="utf-8"))}

def vendor(slug, n):
    key = f"x-{slug}_{n}"; out = os.path.join("_source", key + ".jpg")
    if not os.path.exists(out):
        im = ImageOps.exif_transpose(Image.open(idx[f"{slug}_{n}"]["path"])).convert("RGB")
        im.thumbnail((2000, 2000), Image.LANCZOS)
        im.save(out, quality=88)  # a fresh save carries no EXIF or GPS
    return key

album = json.load(open("data/album.json", encoding="utf-8"))
mill = [vendor(s, n) for s in ("lanark", "clyde") for n in LANARK[s]]
album["newlanark"] = mill[:5] + album.get("newlanark", []) + mill[5:]
wales_old = album.pop("wales", [])
json.dump(album, open("data/album.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

TITLES = [("chester", "Chester", ["chester_4"]), ("conwy", "Conwy and Llandudno", ["llandudno_4", "conwy_4"]),
          ("snowdonia", "Snowdonia and Anglesey", ["snowdonia_2", "snowdonia_5"]),
          ("shrewsbury", "Shrewsbury and Church Stretton", ["shrewsbury_4"]), ("manchester", "Manchester", [])]
extra = [{"title": t, "keys": old + [vendor(s, n) for n in WALES[s]]} for s, t, old in TITLES]
assert set(wales_old) <= {k for g in extra for k in g["keys"]}, "every old Wales album photo moves to the extra section"
json.dump(extra, open("data/extra.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("vendored", len(mill) + sum(len(v) for v in WALES.values()), "photos;", "extra groups:", [(g["title"], len(g["keys"])) for g in extra])
