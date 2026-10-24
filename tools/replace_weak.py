"""Act on the composition audit outside the album: new hero sets and prints from the top-scored picks, every other
weak photo swapped for the best pick from the same folder, and the food photos re-chosen (page-qa food review).
Deletes the position-named photo exports so the build re-crops them. One-time, after tools/make_roll.py."""
import json, os, re, shutil
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
RD = os.path.join(".taste-skill", "roll")
idx = json.load(open(os.path.join(RD, "index.json"), encoding="utf-8"))
weak = {w["site_key"]: w for w in json.load(open(os.path.join(RD, "weak_report.json"), encoding="utf-8"))}
roll = json.load(open("data/roll.json", encoding="utf-8"))
picks = json.load(open("data/picks.json", encoding="utf-8"))
FOOD = {"gla-city_8", "arran_3", "oban_1", "arbroath-docks_6", "aviemore_0", "portree_0", "food_4"}

def key_of(slug, n):
    p = idx["photos"][f"{slug}_{n}"]
    return p["on_site"][0] if p["on_site"] else f"r-{slug}_{n}"
audits = {}
for f in os.listdir(os.path.join(RD, "audit")):
    if f.endswith(".json"):
        audits.update(json.load(open(os.path.join(RD, "audit", f), encoding="utf-8")))
best_in = {slug: [key_of(slug, p["n"]) for p in sorted(v.get("picks", []), key=lambda p: -p.get("score", 4))] for slug, v in audits.items()}
score = {key_of(slug, p["n"]): p.get("score", 4) for slug, v in audits.items() for p in v.get("picks", [])}
portrait = lambda k: (lambda im: im.height > im.width)(Image.open(os.path.join("_source", k + ".jpg")))
used = set()

def top(sections, n, want_portrait=True, avoid=()):
    out = []
    for title, keys in sections:
        for k in sorted(keys, key=lambda k: -score.get(k, 4)):
            if k in avoid or k in used or (want_portrait and not portrait(k)):
                continue
            out.append((k, title)); used.add(k); break
        if len(out) == n:
            break
    return out

trips = roll["trips"]
gla = next(t for t in trips if t["id"] == "glasgow")
gsecs = sorted([(s["title"], [k for k, _ in s["keys"]]) for s in gla["sections"]], key=lambda s: s[0] != "Strathclyde campus")
picks["gstrip"] = [{"file": k, "y": 0.5, "cap": "University of Strathclyde" if t == "Strathclyde campus" else t} for k, t in top(gsecs, 8)]
picks["sstrip"] = [{"file": k, "y": 0.5, "cap": f"{t}, Glasgow"} for k, t in top([s for s in gsecs if s[0] in ("City centre", "The Barras", "Necropolis", "Glasgow Cathedral")], 3)]
others = [(tr["title"] if len(tr["sections"]) == 1 else f"{s['title']}, {tr['title']}" if s["title"] != tr["title"] else tr["title"], [k for k, _ in s["keys"]])
          for tr in trips if tr["id"] != "glasgow" for s in tr["sections"][:1]]
picks["strip"] = [{"file": k, "y": 0.5, "cap": t} for k, t in top(sorted(others, key=lambda s: -max(score.get(k, 4) for k in s[1])), 8)]
pr = top([(t, ks) for t, ks in sorted(others, key=lambda s: -max(score.get(k, 4) for k in s[1]))], 3, want_portrait=False)
picks["prints"] = [{"file": k, "cap": t} for k, t in pr]

# food (page-qa food review): no Portree photo; hero = fish and chips, pudding, roast, burgers
picks["fstrip"] = [{"file": k, "y": 0.5, "cap": c} for k, c in (("arran_3", "Fish and chips with mushy peas, Arran"), ("food_4", "Sticky toffee pudding"),
                                                              ("arbroath-docks_6", "Roast with Yorkshire pudding, Arbroath"), ("aviemore_0", "Burgers and onion rings, Aviemore"))]
picks["food"] = [f for f in picks["food"] if f["file"] != "portree_0"]

# every other weak photo: best pick from the same folder (not a hero/print pick, not used twice)
swap = {}
def repl(k):
    if k in FOOD or k not in weak:
        return k
    if k not in swap:
        cands = [c for c in best_in.get(weak[k]["folder"], []) if c != k and c not in used and c not in weak]
        if cands:
            swap[k] = cands[0]; used.add(cands[0])
    return swap.get(k, k)
picks["intro"] = {name: repl(k) for name, k in picks["intro"].items()}
picks["trips"] = {t: [repl(k) for k in ks] for t, ks in picks["trips"].items()}
json.dump(picks, open("data/picks.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

b = open("tools/build.py", encoding="utf-8").read()
b = b.replace('for i, key in enumerate(["aviemore_0", "oban_1", "arran_3"]):', 'for i, key in enumerate(["oban_1", "aviemore_0"]):')
b = b.replace('"FISH": "portree_0"', '"FISH": "arran_3"')
for k in sorted(set(re.findall(r'"([a-z0-9-]+_\d+)"', b))):
    nk = repl(k)
    if nk != k:
        b = b.replace(f'"{k}"', f'"{nk}"')
open("tools/build.py", "w", encoding="utf-8").write(b)

for d in ("hero", "intro", "verbs", "places", "hs", "shop", "food", "prints", "trips", "og", "around"):
    shutil.rmtree(os.path.join("photos", d), ignore_errors=True)
left = sorted(k for k in set(re.findall(r'"([a-z0-9-]+_\d+)"', b)) | {f["file"] for l in ("gstrip", "strip", "sstrip", "prints") for f in picks[l]}
              | set(picks["intro"].values()) | {k for ks in picks["trips"].values() for k in ks} if k in weak and k not in FOOD)
print("hero School", [f["file"] for f in picks["gstrip"]]); print("hero Travel", [f["file"] for f in picks["strip"]])
print("hero Shopping", [f["file"] for f in picks["sstrip"]]); print("prints", picks["prints"])
print(len(swap), "weak photos swapped;", "still weak (no better pick in that folder):", left)
