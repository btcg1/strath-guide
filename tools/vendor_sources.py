"""Copy the source photos the build uses into _source/ and point tools/build.py at it."""
import json, os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open("tools/build.py", encoding="utf-8").read()
m = re.search(r'^FULL = r"([^"]+)"$', src, re.M)
if m:
    full = m.group(1)
    picks = json.load(open("data/picks.json", encoding="utf-8"))
    keys = set(re.findall(r'"([a-z0-9-]+_\d)"', json.dumps(picks))) | set(re.findall(r'"([a-z0-9-]+_\d)"\)', src))
    os.makedirs("_source", exist_ok=True)
    for k in sorted(keys):
        f = os.path.join(full, k + ".jpg")
        if os.path.exists(f):
            shutil.copy2(f, "_source")
    src = src.replace(m.group(0), 'FULL = os.path.join(ROOT, "_source")')
    src = src.replace("Source photos come from the sampled, EXIF-stripped set in photo_work/full (see FULL below).",
                      "Source photos (resized, EXIF and GPS stripped) live in _source/.")
    open("tools/build.py", "w", encoding="utf-8").write(src)
files = os.listdir("_source")
print(len(files), "source photos,", round(sum(os.path.getsize(os.path.join("_source", f)) for f in files) / 1e6, 1), "MB")
