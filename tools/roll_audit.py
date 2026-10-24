"""Full photo composition audit with Codex: chunked contact sheets (48 per sheet) from the cached thumbnails,
one Codex job per trip (six in parallel). Output: .taste-skill/roll/audit/<trip>.json.
Re-runnable: finished trips are skipped."""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
R = os.path.join(".taste-skill", "roll")
idx = json.load(open(os.path.join(R, "index.json"), encoding="utf-8"))
os.makedirs(os.path.join(R, "chunks"), exist_ok=True); os.makedirs(os.path.join(R, "audit"), exist_ok=True)

def cap(n):
    return 2 if n < 10 else 3 if n < 30 else 4 if n < 60 else 6 if n < 100 else 7 if n < 150 else 9

# group folders by trip (the folder under Ricoh)
trips = {}
for slug, rel in idx["folders"].items():
    parts = rel.replace("\\", "/").split("/")
    trip = re.sub(r"[^a-z0-9]+", "-", re.sub(r"[\d.\s-]+$", "", parts[2]).lower()).strip("-")
    trips.setdefault(trip, []).append(slug)
counts = {s: sum(1 for k in idx["photos"] if k.rsplit("_", 1)[0] == s) for s in idx["folders"]}

font = ImageFont.truetype("arial.ttf", 22); TW = TH = 300; COLS, PER = 8, 48
def chunks(slug):
    out = []
    n = counts[slug]
    for c0 in range(0, n, PER):
        rng = range(c0, min(n, c0 + PER)); rows = (len(rng) + COLS - 1) // COLS
        sh = Image.new("RGB", (COLS * (TW + 6), rows * (TH + 6) + 36), "white"); dr = ImageDraw.Draw(sh)
        dr.text((6, 6), f"{slug}  ({idx['folders'][slug]})  photos {rng[0]}-{rng[-1]}", fill="black", font=font)
        for i, k in enumerate(rng):
            t = Image.open(os.path.join(R, "thumbs", f"{slug}_{k}.jpg")); t.thumbnail((TW, TH))
            x, y = (i % COLS) * (TW + 6), 36 + (i // COLS) * (TH + 6)
            sh.paste(t, (x + (TW - t.width) // 2, y + (TH - t.height) // 2))
            on = idx["photos"][f"{slug}_{k}"]["on_site"]
            dr.rectangle([x, y, x + 50, y + 28], fill="red" if on else "black"); dr.text((x + 5, y + 2), str(k), fill="yellow", font=font)
        p = os.path.join(R, "chunks", f"{slug}-{c0 // PER}.jpg"); sh.save(p, quality=80); out.append(p)
    return out

PROMPT = """Photo composition audit for a travel website's photo album (an exchange student's trip photos, shot on a Ricoh GR).
Attached: numbered contact sheets for these place folders (the folder slug is printed at the top of each sheet):
{folders}
Each thumbnail has its number in the top-left box. RED boxes are photos already used on the website.

For EACH folder:
1. Pick the best photos, at most the cap given above per folder (fewer is fine if quality is lacking). Judge composition strictly:
   a clear subject; strong framing (thirds, leading lines, foreground interest); level horizon/verticals; nothing important cut off;
   good exposure (no near-black or blown-out frames); sharp; no clutter. Prefer variety (one per scene, no near-duplicates,
   mix of wide views and details). Exclude any photo where a person's face is identifiable (distant people or backs are fine),
   screenshots, tickets, receipts, menus, mirror selfies. Red photos may be picked if they are among the best.
2. For every RED photo, give a verdict: "keep" or "weak", with a short reason.

Output ONLY JSON: {{"<slug>": {{"picks": [{{"n": 12, "score": 5, "desc": "3-8 word visual description"}}], "on_site": [{{"n": 3, "verdict": "keep", "why": "..."}}]}}, ...}}
Scores: 5 excellent, 4 good. Do not pick anything below 4. Do not modify any files."""

def run(trip):
    out = os.path.join(R, "audit", f"{trip}.json")
    if os.path.exists(out):
        return trip, "cached"
    slugs = trips[trip]; imgs = [p for s in slugs for p in chunks(s)]
    folders = "\n".join(f"- {s}: {counts[s]} photos, cap {cap(counts[s])}" for s in slugs)
    cmd = ["codex", "exec", "-m", "gpt-6-sol", "-c", 'model_reasoning_effort="high"', "--skip-git-repo-check", "--ephemeral",
           "-s", "read-only"] + sum((["-i", p] for p in imgs), []) + ["-o", out + ".txt", PROMPT.format(folders=folders)]  # -i is greedy: keep -o between the images and the prompt
    r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", timeout=1500)
    txt = open(out + ".txt", encoding="utf-8").read() if os.path.exists(out + ".txt") else ""
    m = re.search(r"\{.*\}", txt, re.S)
    try:
        data = json.loads(m.group(0)); json.dump(data, open(out, "w", encoding="utf-8"), indent=1)
        return trip, f"ok {sum(len(v.get('picks', [])) for v in data.values())} picks"
    except Exception as e:
        return trip, f"FAILED rc={r.returncode} {type(e).__name__} {r.stderr[-300:]}"

only = sys.argv[1:] or list(trips)
print(len(only), "trips:", {t: sum(counts[s] for s in trips[t]) for t in only}, flush=True)
with ThreadPoolExecutor(6) as ex:
    for trip, status in ex.map(run, only):
        print(trip, status, flush=True)
