"""Replace the random photo wall with an album grouped by trip (data/album.json, curated by composition review)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
b = open("tools/build.py", encoding="utf-8").read()
i = b.index("# Wall: curated wall picks plus every trip photo")
j = b.index('R["WALL_COUNT"] = str(len(order))') + len('R["WALL_COUNT"] = str(len(order))')
ALBUM = '''# Album: the photo wall grouped by trip, in date order, Glasgow first (data/album.json holds the curated keys)
album = json.load(open(J("data", "album.json"), encoding="utf-8"))
trip_by_id = {t["id"]: t for t in trips}
group_order = ["glasgow"] + [t["id"] for t in trips if t["id"] in album]
blocks, order = [], []
for gid in group_order:
    keys = [k for k in album.get(gid, []) if k not in {p["file"] for p in picks["prints"]}]
    if not keys: continue
    if gid == "glasgow":
        title, when = "Glasgow", "all semester"
    else:
        t = trip_by_id[gid]; title = t["name"]
        when = nice_date(t["date"]) + (f" – {nice_date(t['end'])}" if t["end"] else "")
    figs = []
    for key in keys:
        order.append(key)
        src, w, h = export(key, f"wall/{key}.jpg", None, (700, 1050))
        name = caption(key).split(",")[0]
        figs.append(f'<figure data-large="{large(key)}">{img(src, w, h, caption(key))}<figcaption>{esc(name)}</figcaption></figure>')
    blocks.append(f'<div class="album__group"><h3 class="album__title">{esc(title)} <span>{esc(when)}</span></h3><div class="album__grid">{"".join(figs)}</div></div>')
R["WALL"] = "\\n    ".join(blocks)
R["WALL_COUNT"] = str(len(order))'''
b = b[:i] + ALBUM + b[j:]
open("tools/build.py", "w", encoding="utf-8").write(b)

t = open("src/travel.html", encoding="utf-8").read()
t2 = re.sub(r'  <div class="wall" data-wall>\n    \{\{WALL\}\}\n  </div>\n  <div class="wall__more">.*?</div>\n',
            '  <div class="album">\n    {{WALL}}\n  </div>\n', t, flags=re.S)
assert t2 != t, "wall block not found"
open("src/travel.html", "w", encoding="utf-8").write(t2)

j_ = open("js/site.js", encoding="utf-8").read()
j_ = j_.replace("() => $$('.wall figure:not([hidden])')", "() => $$('.album figure')")
open("js/site.js", "w", encoding="utf-8").write(j_)

c = open("css/site.css", encoding="utf-8").read()
c += """
/* Album: one group per trip, in date order */
.album { padding: 72px var(--m) 0; display: grid; gap: 64px; }
.album__group { display: grid; grid-template-columns: minmax(0, 15rem) minmax(0, 1fr); gap: 16px calc(var(--gutter) * 2); align-items: start; content-visibility: auto; contain-intrinsic-size: auto 520px; }
.album__title { font-size: var(--step-lead); line-height: 1.1; position: sticky; top: 24px; }
.album__title span { display: block; margin-top: 6px; font-family: var(--text-face); font-size: var(--step-small); letter-spacing: 0.01em; color: var(--muted); }
.album__grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.album__grid figure { margin: 0; cursor: zoom-in; }
.album__grid img { width: 100%; aspect-ratio: 2 / 3; object-fit: cover; background: var(--surface); }
.album__grid figcaption { font-size: var(--step-small); color: var(--muted); padding-top: 6px; }
@media (hover: hover) and (pointer: fine) { .album__grid img { transition: opacity var(--t-hover) ease; } .album__grid figure:hover img { opacity: 0.88; } }
@media (max-width: 860px) {
  .album { gap: 48px; }
  .album__group { grid-template-columns: minmax(0, 1fr); }
  .album__title { position: static; }
  .album__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
}
"""
open("css/site.css", "w", encoding="utf-8").write(c)
print("album patched")
