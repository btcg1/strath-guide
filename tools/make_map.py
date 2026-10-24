"""Build a lightweight SVG land outline of Great Britain, Ireland and the Isle of Man from Natural Earth (via world-atlas).

Writes data/map.json: {"lon0", "lat0", "k", "paths": [svg path d], "bbox": [x0, y0, x1, y1]}.
Projection: x = (lon - lon0) * k * 100, y = -(lat - lat0) * 100, with k = cos(lat0). The page uses the same numbers.
"""
import json, math, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "countries-10m.json")
URL = "https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-10m.json"
IDS = {"826", "372", "833"}            # United Kingdom, Ireland, Isle of Man
LON0, LAT0 = -4.0, 56.0
K = math.cos(math.radians(LAT0))
BOX = (-11.0, 49.8, 2.2, 61.0)          # lon/lat clip box
TOL = 0.006                              # simplification tolerance, in degrees of latitude

if not os.path.exists(CACHE):
    urllib.request.urlretrieve(URL, CACHE)
topo = json.load(open(CACHE, encoding="utf-8"))
sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]

def arc(i):
    a = topo["arcs"][i if i >= 0 else ~i]
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))
    return pts if i >= 0 else pts[::-1]

def ring(idx):
    pts = []
    for i in idx:
        p = arc(i)
        pts.extend(p[1:] if pts else p)
    return pts

def proj(lon, lat):
    return ((lon - LON0) * K * 100, -(lat - LAT0) * 100)

def dp(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1e-12
        best, bi = 0, -1
        for i in range(a + 1, b):
            x0, y0 = pts[i]
            d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / L
            if d > best: best, bi = d, i
        if best > tol and bi > 0:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

paths, n_in, n_out = [], 0, 0
for g in topo["objects"]["countries"]["geometries"]:
    if str(g.get("id")) not in IDS: continue
    polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
    for poly in polys:
        for r in poly[:1]:                      # outer rings only; lakes are not needed at this scale
            pts = ring(r)
            if not any(BOX[0] <= x <= BOX[2] and BOX[1] <= y <= BOX[3] for x, y in pts): continue
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            if (max(xs) - min(xs)) * K < 0.02 and (max(ys) - min(ys)) < 0.02: continue   # drop specks
            P = [proj(x, y) for x, y in pts]
            # a closed ring starts and ends on the same point, so split it at its farthest point first
            far = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)
            S = dp(P[:far + 1], TOL * 100) + dp(P[far:], TOL * 100)[1:]
            n_in += len(P); n_out += len(S)
            if len(S) < 4: continue
            paths.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in S) + "Z")
x0, y0 = proj(BOX[0], BOX[3]); x1, y1 = proj(BOX[2], BOX[1])
json.dump({"lon0": LON0, "lat0": LAT0, "k": K, "paths": paths, "bbox": [x0, y0, x1, y1]},
          open(os.path.join(ROOT, "data", "map.json"), "w"), separators=(",", ":"))
size = os.path.getsize(os.path.join(ROOT, "data", "map.json")) / 1024
print(f"{len(paths)} shapes, {n_in} -> {n_out} points, map.json {size:.0f} KB")
