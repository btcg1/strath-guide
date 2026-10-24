"""Softer ground and chapter fields; redesigned intros on both pages."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
def patch(path, pairs):
    s = open(path, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, s.count(a), a[:80]); s = s.replace(a, b)
    open(path, "w", encoding="utf-8").write(s)
def swap_section(path, start, new):
    s = open(path, encoding="utf-8").read()
    i = s.index(start); j = s.index("</section>", i) + len("</section>")
    open(path, "w", encoding="utf-8").write(s[:i] + new + s[j:])

# Travel intro: four prints whose captions finish the sentence
swap_section("src/travel.html", '<section class="intro"', '''<section class="intro intro--roll" aria-label="Introduction">
  <p class="intro__lead" data-reveal>One semester in Glasgow looked like this:</p>
  <div class="intro__row">
    <figure><img src="{{INTRO_CAMPUS}}" alt="Glasgow Cathedral" width="640" height="800" loading="lazy"><figcaption>Lectures by the cathedral,</figcaption></figure>
    <figure><img src="{{INTRO_HAGGIS}}" alt="Haggis, neeps and tatties" width="640" height="800" loading="lazy"><figcaption>haggis for lunch,</figcaption></figure>
    <figure><img src="{{INTRO_FERRY}}" alt="Boat on the Firth of Forth" width="640" height="800" loading="lazy"><figcaption>ferries at dawn</figcaption></figure>
    <figure><img src="{{INTRO_SKYE}}" alt="Old Man of Storr, Skye" width="640" height="800" loading="lazy"><figcaption>and 24 trips out of Glasgow.</figcaption></figure>
  </div>
</section>''')

# Guide intro: who wrote this, and how to use the two tabs
swap_section("src/guide.html", '<section class="intro" aria-label="The four steps">', '''<section class="intro intro--who" aria-label="Who wrote this">
  <p class="intro__lead" data-reveal>We did semester 1 at Strathclyde in 2025. This is everything we wish someone had told us first.</p>
  <div class="intro__cols">
    <p>This tab is the boring-but-important stuff, in the order you'll need it: applying through NTU, course matching, getting into the UK, money, halls, food, and all the questions we kept asking each other. Every price and date was checked against the official page in October 2026, and the links take you straight there.</p>
    <p>The <a href="travel.html">Travel tab</a> is the fun part: the 24 trips we managed in one semester, 36 places with prices and opening times, and way too many photos. Strath is in an amazing spot for travelling, so make the most of it.</p>
  </div>
</section>''')

# Bigger 4:5 intro photos
patch("tools/build.py", [
 ('    src, w, h = export(key, f"intro/{k}.jpg", 4 / 3, (300, 225))\n    R["INTRO_" + k.upper()] = src',
  '    src, w, h = export(key, f"intro/{k}-p.jpg", 4 / 5, (640, 800))\n    R["INTRO_" + k.upper()] = src'),
])

css = open("css/site.css", encoding="utf-8").read()
css = css.replace("""  --bg: #ffffff;
  --surface: #f2f3f5;
  --ink: #111111;
  --muted: #5f6368;""", """  --bg: #eef1ee;          /* haar: a soft sea-mist grey, easier on the eyes than white */
  --surface: #e2e7e3;     /* one tone step down, for chapter fields */
  --paper: #f7f8f6;       /* lighter step, for maps and inputs */
  --ink: #141816;
  --muted: #56605b;
  --field-2: #17312c;     /* deep loch green */
  --field-2-ink: #eef1ee;
  --field-2-soft: #9fb5ad;
  --field-2-link: #a8cdf0;""", 1)
assert "--field-2: #17312c" in css
# remove the old centred-statement intro rules, add the two new intros
css = re.sub(r"/\* Intro statement with inline frames \*/.*?(?=\n/\* Trips map \*/)", """/* Intros */
.intro { padding: 96px var(--m) var(--section); }
.intro__lead { font-family: var(--display-face); font-size: var(--step-lead); line-height: 1.15; letter-spacing: -0.01em; max-width: 26ch; }
.intro--roll { display: grid; gap: 40px; }
.intro__row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--gutter); align-items: start; }
.intro__row figure { margin: 0; display: grid; gap: 14px; }
.intro__row figure:nth-child(even) { margin-top: 72px; }
.intro__row img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; }
.intro__row figcaption { font-family: var(--display-face); font-size: var(--step-lead); line-height: 1.1; letter-spacing: -0.01em; }
.intro--who { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 28px calc(var(--gutter) * 2); align-items: start; }
.intro__cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--gutter) calc(var(--gutter) * 1.5); }
.intro__cols p { max-width: 46ch; }
@media (max-width: 860px) {
  .intro { padding-block: 64px 96px; }
  .intro__row { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 12px; }
  .intro__row figure:nth-child(even) { margin-top: 40px; }
  .intro__row figcaption { font-size: 1.25rem; }
  .intro--who, .intro__cols { grid-template-columns: minmax(0, 1fr); }
}
""", css, count=1, flags=re.S)
assert "/* Intros */" in css
pairs = [
 # map: pale-blue sea, light land
 ("#map { position: absolute; inset: 0; width: 100%; height: 100%; display: block; background: #ffffff; }",
  "#map { position: absolute; inset: 0; width: 100%; height: 100%; display: block; background: #dbe5ea; }"),
 (".mland path { fill: #e4e7eb; stroke: #c9ced5;", ".mland path { fill: var(--paper); stroke: #b9c4c9;"),
 (".mpin { fill: var(--ink); stroke: #fff;", ".mpin { fill: var(--ink); stroke: var(--paper);"),
 (".mlabel { font-family: var(--display-face); fill: var(--ink); paint-order: stroke; stroke: #fff;", ".mlabel { font-family: var(--display-face); fill: var(--ink); paint-order: stroke; stroke: var(--paper);"),
 (".trips__map { position: sticky; top: 24px; height: calc(100svh - 48px); min-height: 480px; background: var(--surface); }",
  ".trips__map { position: sticky; top: 24px; height: calc(100svh - 48px); min-height: 480px; background: #dbe5ea; }"),
 # costs on a deep green field
 (".costs { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--gutter) calc(var(--gutter) * 2); padding: var(--section) var(--m) 0; align-items: center; }",
  ".costs { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--gutter) calc(var(--gutter) * 2); padding: var(--section) var(--m); align-items: center; background: var(--field-2); color: var(--field-2-ink); }\n.costs .soft { color: var(--field-2-soft); }\n.costs a { color: var(--field-2-link); }\n.costs .conv input { background: rgba(255, 255, 255, 0.08); color: var(--field-2-ink); border-bottom-color: var(--field-2-ink); }\n.costs .conv output { color: var(--field-2-link); }\n.costs ::selection { background: var(--field-2-link); color: var(--field-2); }"),
 # dates and the season chart on the tone-step field
 (".dates { padding: var(--section) var(--m) 0; }", ".dates { padding: var(--section) var(--m); margin-top: var(--section); background: var(--surface); }\n.dates + .costs { padding-top: var(--section); }"),
 (".year { padding: var(--section) var(--m) 0; display: grid; gap: 64px; }", ".year { padding: var(--section) var(--m); margin-top: var(--section); display: grid; gap: 64px; background: var(--surface); }\n.year .track { background: var(--paper); }"),
 (".roll__field { position: relative; min-height: 100svh; background: var(--surface);", ".roll__field { position: relative; min-height: 100svh; background: var(--field-2);"),
 (".roll__title { display: grid; justify-items: center; font-size: var(--step-display);", ".roll__title { display: grid; justify-items: center; color: var(--field-2-ink); font-size: var(--step-display);"),
 (".roll__note { position: absolute; left: var(--m); bottom: 24px; font-size: var(--step-body); max-width: 40ch; }", ".roll__note { position: absolute; left: var(--m); bottom: 24px; font-size: var(--step-body); max-width: 40ch; color: var(--field-2-ink); }"),
 (".conv input { width: 4.2em; font: inherit; color: var(--ink); background: var(--surface);", ".conv input { width: 4.2em; font: inherit; color: var(--ink); background: var(--paper);"),
 (".faq details[open] { background: var(--surface);", ".faq details[open] { background: var(--paper);"),
]
for a, b in pairs:
    assert css.count(a) == 1, (css.count(a), a[:80]); css = css.replace(a, b)
open("css/site.css", "w", encoding="utf-8").write(css)
print("restyled")
