"""Check every external link on the built pages. Usage: python tools/linkcheck.py  (prints only failures)"""
import os, re, ssl, urllib.request
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = set()
for page in ("index.html", "travel.html"):
    urls |= set(re.findall(r'href="(https?://[^"]+)"', open(os.path.join(ROOT, page), encoding="utf-8").read()))
urls = {u.replace("&amp;", "&") for u in urls if "fonts.g" not in u}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def check(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "text/html,*/*"}), timeout=20, context=ssl.create_default_context())
        return u, r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return u, e.code, ""
    except Exception as e:
        return u, type(e).__name__, ""
res = list(ThreadPoolExecutor(16).map(check, sorted(urls)))
bad = [r for r in res if r[1] != 200]
print(len(res), "links,", len(bad), "not 200")
for u, s, _ in bad: print(s, u)
