"""Turn the composition audit (.taste-skill/roll/audit/*.json) into data/roll.json for the Photos tab.
Vendors picked photos from Drive into _source/ as r-<folder>_<n> (2000px, no EXIF), reusing the site's own copy when a pick
is already on the site. Also swaps audit-flagged weak photos out of the Travel trip cards, and writes a report of the
remaining weak on-site photos to .taste-skill/roll/weak_report.json. Re-runnable."""
import json, os, re
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
R = os.path.join(".taste-skill", "roll")
idx = json.load(open(os.path.join(R, "index.json"), encoding="utf-8"))
trips = json.load(open("data/trips.json", encoding="utf-8")); tby = {t["id"]: t for t in trips}
picks = json.load(open("data/picks.json", encoding="utf-8"))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
nice = lambda iso: f"{int(iso[8:])} {MONTHS[int(iso[5:7]) - 1]}"

TRIP_ID = {"oban": "oban", "glenfinnan": "glenfinnan", "falkirk": "falkirk", "inchcolm": "inchcolm", "loch-ness": "lochness",
           "arbroath": "arbroath", "hamilton": "hamilton", "preston-mill": "prestonmill", "stirling": "stirling", "skye": "skye",
           "culross": "culross", "dunnottar": "dunnottar", "st-andrews": "standrews", "lomund-hill-house": "lomond",
           "argyll-forest": "argyll", "dunkeld": "dunkeld", "arran": "arran", "new-lanark": "newlanark", "edinburgh": "edinburgh",
           "inverness": "inverness", "aberdeen": "aberdeen", "northern-ireland": "ni", "chester": "wales", "york": "york"}
SEC = {"glasgow-uog": "University of Glasgow", "glasgow-pollock": "Pollok Country Park", "glasgow-pollock-art-museum": "Pollok Country Park",
       "glasgow-strath": "Strathclyde campus", "glasgow-city": "City centre", "glasgow-barras": "The Barras", "glasgow-necropolis": "Necropolis",
       "glasgow-cathedral": "Glasgow Cathedral", "glasgow-kelvingrove": "Kelvingrove", "glasgow-riverside-museum": "Riverside Museum",
       "oban-st-conan-s-kirk-kilchurn": "St Conan's Kirk and Kilchurn Castle", "oban-rest-and-be-thankful-tarbet": "Rest and Be Thankful and Tarbet",
       "glenfinnan-viaduct": "Glenfinnan Viaduct", "loch-ness-commando": "Commando Memorial", "dunnottar-dundee-toilet": "Dundee",
       "skye-creag-an-fh-ilidh": "Creag an Fhèilidh", "inverness-rothiemurcus": "Rothiemurchus", "lomund-hill-house-loch-lomund": "Loch Lomond",
       "argyll-forest-rest-and-be-thankful": "Rest and Be Thankful", "aberdeen-alford-grampian": "Grampian Transport Museum, Alford",
       "aberdeen-alford-heritage-museum": "Alford Heritage Museum", "aberdeen-alford-alford": "Alford",
       "northern-ireland-giant-s-causeway-dark-hedges": "Giant's Causeway and the Dark Hedges", "chester-conwy-llandudno": "Conwy and Llandudno",
       "chester-snowdonia-llanfairpwll": "Snowdonia and Llanfairpwll", "chester-shrewsbury-church-stretton": "Shrewsbury and Church Stretton",
       "chester-manchester-mill": "Manchester", "york-rail-museum": "National Railway Museum", "york": "York",
       "inverness-culloden-fort-george": "Culloden and Fort George", "aberdeen-university-of-aberdeen": "University of Aberdeen"}

def sec_title(slug):
    if slug in SEC:
        return SEC[slug]
    last = idx["folders"][slug].replace("\\", "/").split("/")[-1]
    return re.sub(r"\s*[\d.]+(\s*-\s*[\d.]+)?$", "", last).replace(" + ", " and ").replace("&", "and").strip()

def vendor(slug, n):
    p = idx["photos"][f"{slug}_{n}"]
    if p["on_site"]:
        return p["on_site"][0]
    key = f"r-{slug}_{n}"; out = os.path.join("_source", key + ".jpg")
    if not os.path.exists(out):
        im = ImageOps.exif_transpose(Image.open(p["path"])).convert("RGB"); im.thumbnail((2000, 2000), Image.LANCZOS); im.save(out, quality=88)
    return key

groups, weak = {}, []
for f in sorted(os.listdir(os.path.join(R, "audit"))):
    if not f.endswith(".json"):
        continue
    trip = f[:-5]; data = json.load(open(os.path.join(R, "audit", f), encoding="utf-8"))
    for slug, v in data.items():
        if slug not in idx["folders"]:
            print("unknown slug", slug); continue
        keys = [(vendor(slug, p["n"]), p.get("desc", ""), p.get("score", 4)) for p in sorted(v.get("picks", []), key=lambda p: -p.get("score", 4))]
        if keys:
            groups.setdefault(trip, []).append({"slug": slug, "title": sec_title(slug), "keys": keys})
        for o in v.get("on_site", []):
            if o.get("verdict") == "weak":
                weak += [{"site_key": k, "folder": slug, "n": o["n"], "why": o.get("why", "")} for k in idx["photos"][f"{slug}_{o['n']}"]["on_site"]]

order = sorted(groups, key=lambda t: "0" if t == "glasgow" else tby[TRIP_ID[t]]["date"])
out = {"all": len(idx["photos"]), "trips": [], "hero": []}
for t in order:
    if t == "glasgow":
        tid, title, when = "glasgow", "Glasgow", "all semester"
    else:
        tr = tby[TRIP_ID[t]]; tid, title = tr["id"], tr["name"]
        when = nice(tr["date"]) + (f" – {nice(tr['end'])}" if tr.get("end") else "")
    secs = groups[t]
    merged = {}
    for s in secs:  # folders that share a title (e.g. two Pollok folders) become one section
        merged.setdefault(s["title"], []).extend(s["keys"])
    out["trips"].append({"id": tid, "title": title, "when": when,
                         "sections": [{"title": k, "keys": [[key, desc] for key, desc, _ in v]} for k, v in merged.items()]})

# hero: the strongest portrait frames, one per trip
seen = set()
for tr in out["trips"]:
    for s in tr["sections"]:
        for key, desc in s["keys"]:
            im = Image.open(os.path.join("_source", key + ".jpg"))
            if im.height > im.width and tr["id"] not in seen and len(out["hero"]) < 8:
                out["hero"].append({"file": key, "y": 0.5, "cap": f"{s['title']}, {tr['title']}" if s["title"] != tr["title"] else tr["title"]}); seen.add(tr["id"])
json.dump(out, open("data/roll.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# trip cards on the Travel tab: replace audit-flagged weak photos with that trip's best picks
weak_keys = {w["site_key"] for w in weak}
swapped = []
for t in order:
    if t == "glasgow":
        continue
    tid = TRIP_ID[t]; cur = picks["trips"].get(tid, [])
    best = [k for s in groups[t] for k, _, sc in s["keys"] if sc >= 5 and k not in cur] + [k for s in groups[t] for k, _, sc in s["keys"] if sc == 4 and k not in cur]
    new = []
    for k in cur:
        if k in weak_keys and best:
            nk = best.pop(0); new.append(nk); swapped.append((tid, k, nk))
        else:
            new.append(k)
    picks["trips"][tid] = new
json.dump(picks, open("data/picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(weak, open(os.path.join(R, "weak_report.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
n = sum(len(s["keys"]) for tr in out["trips"] for s in tr["sections"])
print(f"roll: {len(out['trips'])} trips, {n} photos, hero {len(out['hero'])}; weak on-site photos: {len(weak)}; trip-card swaps: {len(swapped)}")
for s in swapped: print("  swap", s)
