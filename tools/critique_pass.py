"""Round-5 critique fixes (page-qa juror + Codex design audit + Codex copy edit)."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
missing = []
def soft(path, pairs):
    p = os.path.join(ROOT, path); s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        n = s.count(a)
        if n == 0: missing.append((path, a[:70])); continue
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)

# ---------- copy edits (Codex), facts unchanged ----------
soft("src/guide.html", [
 ("Everything we wish someone had told us before our semester at Strathclyde: applying, course matching, the ETA, money, halls and daily life in Glasgow.",
  "Going to Strathclyde? Here's what we learnt about applying, course matching, the ETA, money, halls and daily life in Glasgow."),
 ("We did semester 1 at Strathclyde in 2025. This is everything we wish someone had told us first.", "We spent semester 1 at Strathclyde in 2025. Here's what we'd tell a friend going next."),
 ("This tab is the boring-but-important stuff, in the order you'll need it: applying through NTU, course matching, getting into the UK, money, halls, food, and all the questions we kept asking each other.",
  "Start here for the stuff you'll need, in order: applying through NTU, course matching, getting into the UK, money, halls, food and the questions we kept asking each other."),
 ("Every price and date was checked against the official page in October 2026, and the links take you straight there.", "We checked prices and dates against the official pages in October 2026. Use the links to check again before you book."),
 ("Every station is a short walk&nbsp;away", "Getting around from&nbsp;campus"),
 ('<p class="tablename">Further</p>', '<p class="tablename">Beyond Glasgow</p>'),
 ("December gets about 33 hours of sunshine in the whole month. It rains more than 60 mm every month, so a good waterproof jacket is the first thing to buy.",
  "December gets about 33 hours of sunshine all month. Rain tops 60 mm every month, so bring a good waterproof jacket."),
 ("Perfect for St Andrews and the Fife coast.", "Handy for St Andrews and the Fife coast."),
 ("Everything here we tried ourselves, so it's subjective.", "We tried everything here ourselves, so this is just our take."),
 ("<td>Cheap fine dining</td>", "<td>Student-run fine dining</td>"),
 ("Cheap, vegetarian friendly, good quality.", "Cheap, good falafel, and vegetarian friendly."),
 ("Local food with really good ingredients.", "Scottish food made with really good ingredients."),
 ("Our one expensive rec: a very good Sunday roast, close to school.", "Our one pricier pick: a very good Sunday roast close to school."),
 ("Glasgow has loads of good brunch spots in the centre and West End.", "Glasgow has loads of brunch spots in the centre and West End."),
 ("Not that common in Singapore, so worth trying.", "We don't see Lebanese food as often in Singapore, so give it a go."),
 ("<td>Sweet and savoury.</td>", "<td>Sweet and savoury pancakes.</td>"),
 ("Whenever you crave Chinese food and don't want to cook, there are lots of options.", "Craving Chinese food and don't want to cook? Try the West End."),
 ("East Sands. So good.", "East Sands. Worth a stop for a toastie."),
 ("South St. Also so good.", "South St. Save room for gelato."),
 ("The things we were glad we brought:", "Here's what we were glad we packed:"),
 ("or any shoes with real grip.", "or any shoes with a good grip."),
 ("Each one is a draft for a week, then final", "Each timetable stays in draft for a week before it's final"),
 ("Mixed flats mean more people: more fun, but a higher chance of a bad flatmate.", "Mixed flats have more people. That can be fun, but there's also more chance of a flatmate you don't click with."),
 ("<summary>Which SIM card?</summary>", "<summary>Which SIM should I get?</summary>"),
 ("And everyone jaywalks, but the lights work very differently from Singapore's, so watch them for a few days first.",
  "Everyone jaywalks here, but the traffic lights work differently from Singapore's. Give yourself a few days to get used to them."),
 ('<a class="button" href="#apply">Read the four steps</a>', '<a class="button" href="#apply">Start with applying</a>'),
])
soft("src/travel.html", [
 ("Every weekend we could, we left Glasgow. Here's where we went: 24 trips on a map, 36 places with prices and opening times, and way too many photos.",
  "Whenever we could, we left Glasgow. Here's our map of 24 trips, plus 36 places with prices and opening times, and way too many photos."),
 ("One semester in Glasgow looked like this:", "Our semester went something like this:"),
 ("Point at a row to see it.", "Pick a place to preview its photo."),
 ("Drag through the weeks.", "Drag the slider through the weeks."),
 ("Arrive in September for the end of the season, in January for the start of the next.", "Arriving in September? You'll catch the end of the season. January arrivals catch the start of the next."),
 ("Thirty-six places, with how to get there, when they open and what they cost.", "Thirty-six places, with travel details, opening times and prices."),
 ("Prices, ferry seasons and opening times on this page were checked against each official site on 24–25 October 2026. They change every year, so check before you book.",
  "We checked prices, ferry seasons and opening times on the official sites on 24–25 October 2026. They change every year, so check again before you book."),
])
soft("tools/build.py", [
 ('("match", "Match",', '("match", "Match courses",'), ('("fly", "Fly",', '("fly", "Before you fly",'), ('("settle", "Settle",', '("settle", "Settle in",'),
 ("You need two NTU semesters done, a CGPA of 3.3 or more, and no earlier in-person exchange.", "You need to have finished two NTU semesters, have a CGPA of 3.3 or above, and not have been on an in-person exchange before."),
 ("NTU does the nominating; you just wait for Strath's email.", "NTU sends your nomination. Then keep an eye out for Strath's email."),
 ("Honestly, don't stress: NTU is known at Strath for being a headache to course-match, so the coordinators are flexible as long as most of your classes are in your primary department.",
  "Honestly, don't stress too much. Strath's coordinators know NTU course matching can be a headache, and they're flexible as long as most of your classes are in your primary department."),
 ("It's usually decided within a day, but give it 3 working days.", "It usually comes through within a day, but give it 3 working days."),
 ("Right after, there's a free market of stuff past students left behind (cutlery, plates, decor, storage), so take what you need.",
  "After you collect your keys, check the free market of cutlery, plates, decor and storage left by past students. Take what you need."),
 ("Then TJ Hughes in the St Enoch Centre for bedding, pans and a laundry basket.", "Then head to TJ Hughes in the St Enoch Centre for bedding, pans and a laundry basket."),
 ("1 March – 15 May for a September start and 15 September – 15 October for January.", "<span class=\"n\">1 March – 15 May</span> for a September start and <span class=\"n\">15 September – 15 October</span> for January."),
 ("ESN Strathclyde runs weekend tours for about £45, picked up from campus. Last year's code was ESN25.", "ESN Strathclyde's weekend tours cost about £45 and pick you up from campus. Last year's code was ESN25."),
 ("Flixbus is usually the cheapest, and 20% less with Student Beans.", "Flixbus is usually the cheapest. Student Beans gets you 20% off."),
 ('"Year-round. Eilean Donan shut all January"', '"Year-round. Eilean Donan is shut all January"'),
 ('"Activities priced separately"', '"Pay for activities separately"'), ('"Loch free"', '"Free to visit the loch"'), ('"Free to wander"', '"Free to explore"'),
 ('"Museum from 10:00 or 11:00"', '"Museum opens at 10:00 or 11:00"'),
 ("A must, even though it's annoying to get to.", "Getting to Glencoe is annoying, but honestly, go."),
 ("A surreal place. It's a steep walk down from the station.", "The mill village feels surreal, and the walk down from the station is steep."),
 ("Proper village vibes, farmers' markets and a very modern bakery.", "Farmers' markets, proper village vibes and a bakery that feels surprisingly modern."),
 ("Only for the very adventurous: remote and peaceful, with a lovely coastal walk.", "If you like remote, peaceful places, the coastal walk is lovely."),
 ("Calton Hill and its café are a nice chill spot. Bertie's might be the best fish and chips in Scotland.", "Calton Hill is a nice place to chill, and there's a café. Bertie's might be the best fish and chips in Scotland."),
])
t = json.load(open("data/trips.json", encoding="utf-8"))
NEW = {"oban": "One ESN day tour we'd recommend: Oban under McCaig's Tower, with Inveraray and Kilchurn Castle on the way.",
       "lochness": "It's a long ESN day, but you get Glencoe, the Commando Memorial, Fort Augustus and Urquhart Castle.",
       "arbroath": "Walk the coast for red sandstone cliffs and sea stacks.", "hamilton": "Glasgow's nearest racecourse.",
       "stirling": "The castle and Wallace Monument are both up very steep hills. Give yourself more time than you think.",
       "dunnottar": "The clifftop castle ruin is a coastal walk from Stonehaven.",
       "newlanark": "A surreal mill village by the Falls of Clyde, with a steep walk from the station.",
       "argyll": "We went via Dunoon and Glenbranter to the Rest and Be Thankful."}
for x in t:
    if x["id"] in NEW: x["line"] = NEW[x["id"]]
json.dump(t, open("data/trips.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- hero: word-sized strip, pitch beside line 2 ----------
def hero_body(w1, w2, P, lead, actions):
    return (f'<div class="hero__body">\n    <h1 class="hero__title">\n      <span class="hero__line"><span class="hero__word">{w1}</span>\n'
            f'        <span class="stripwrap"><span class="strip shutter" data-strip>\n          {{{{{P}STRIP_IMGS}}}}\n'
            f'        </span><span class="strip__caption" data-strip-caption>{{{{{P}STRIP_CAPTION0}}}}</span></span></span>\n'
            f'      <span class="hero__line hero__line--2"><span class="hero__word">{w2}</span></span>\n    </h1>\n'
            f'    <div class="hero__pitch">\n      <p class="hero__lead">{lead}</p>\n      {actions}\n    </div>\n  </div>\n</header>')
for path, w1, w2, P in [("src/guide.html", "Semester at", "Strathclyde", "G_"), ("src/travel.html", "Trips from", "Glasgow", "")]:
    s = open(path, encoding="utf-8").read()
    i = s.index('<div class="hero__body">'); j = s.index("</header>", i) + len("</header>")
    old = s[i:j]
    lead = re.search(r'<p class="hero__lead">(.*?)</p>', old, re.S).group(1)
    actions = re.search(r'<div class="hero__actions">.*?</div>', old, re.S).group(0)
    s = s[:i] + hero_body(w1, w2, P, lead, actions) + s[j:]
    open(path, "w", encoding="utf-8").write(s)

# ---------- panels: sharp portrait photo beside the text ----------
soft("tools/build.py", [
 ('''    d, dw, dh = export(key, f"verbs/{vid}-d.jpg", 16 / 9, (1600, 900), dark=0.64)
    m, mw, mh = export(key, f"verbs/{vid}-m.jpg", 9 / 16, (900, 1600), dark=0.64)''',
  '''    d, dw, dh = export(key, f"verbs/{vid}-p.jpg", 4 / 5, (1066, 1333))'''),
 ('''<picture><source media="(max-width: 720px)" srcset="{m}">'
                  f'{img(d, dw, dh, caption(key))}</picture>''',
  '''<figure class="panel__pic">'
                  f'{img(d, dw, dh, caption(key))}</figure>'''),
])

css = open("css/site.css", encoding="utf-8").read()
css = css.replace("  --step-lead: clamp(1.375rem, 1.05rem + 1.3vw, 2.25rem);", "  --step-lead: clamp(1.25rem, 0.8rem + 1.1vw, 1.875rem);")
css += r"""
/* ---------- Round 5: critique fixes ---------- */
/* Bodoni hairlines: a smaller optical size keeps the thin strokes visible at display sizes */
h1, h2, .hero__title, .roll__title, .foot__mark, .ledger__row, .statement, .intro__lead, .intro__row figcaption, .index__name, .trip-card__name, .why, .foot__invite { font-optical-sizing: none; font-variation-settings: "opsz" 28; }

/* Hero v2: the strip is a word, the pitch fills the space beside line two */
.hero { min-height: 0; padding: 22px var(--m) 72px; }
.hero__body { display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 1.15fr); align-content: start; padding-block: clamp(56px, 9vh, 120px) 0; justify-items: stretch; }
.hero__title { grid-area: 1 / 1 / 2 / -1; font-size: clamp(4.25rem, 1rem + 8.4vw, 10.5rem); line-height: 0.94; }
.hero__line { justify-content: flex-start; }
.hero__line--2 { margin-top: 0.12em; }
.stripwrap { flex: 0 0 clamp(300px, 34vw, 660px); height: 0.74em; }
.strip { border-radius: 0.07em; }
.strip__caption { top: calc(100% + 8px); right: auto; left: 0; text-align: left; }
.hero__pitch { grid-area: 1 / 2; align-self: end; z-index: 1; display: grid; gap: 22px; padding-bottom: 0.4rem; }
.hero__lead { margin: 0; max-width: 34ch; text-align: left; font-size: var(--step-body); line-height: 1.5; }
.hero__actions { margin: 0; }
@media (max-width: 1100px) {
  .hero__body { grid-template-columns: minmax(0, 1fr); }
  .hero__pitch { grid-area: auto; margin-top: 40px; }
}
@media (max-width: 720px) {
  .hero { padding: 16px var(--m) 40px; }
  .hero__body { padding-block: 32px 0; }
  .hero__title { font-size: 15vw; }
  .stripwrap { flex: 0 0 100%; height: auto; aspect-ratio: 3 / 1; margin-block: 0.12em 0.3em; }
  .stripwrap .strip__caption { display: none; }
  .hero__pitch { margin-top: 28px; gap: 20px; }
}
@media (prefers-reduced-motion: no-preference) {
  .js .hero__word { animation: none; }
  .js .hero__pitch { animation: up 600ms var(--ease-out) 300ms both; }
  .js .hero__actions { animation: none; }
}

/* Step panels v2: portrait photo beside the text, on the loch-green field */
.panel { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-areas: "pic verb" "pic facts"; grid-template-rows: 1fr auto; height: auto; min-height: min(88svh, 960px); background: var(--field-2); color: var(--field-2-ink); }
.panel:nth-child(even) { grid-template-areas: "verb pic" "facts pic"; }
.panel__pic { grid-area: pic; position: relative; margin: 0; min-height: 520px; }
.panel__pic img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.panel__verb { grid-area: verb; position: static; inset: auto; display: block; align-self: end; padding: 64px clamp(24px, 5vw, 88px) 20px; text-align: left; font-size: var(--step-head); line-height: 1; }
.panel__facts { grid-area: facts; position: static; max-width: 60ch; background: none; padding: 0 clamp(24px, 5vw, 88px) 72px; }
.panel__facts a { color: var(--field-2-link); }
.panel + .panel { border-top: 0; }
@media (max-width: 720px) {
  .panel, .panel:nth-child(even) { grid-template-columns: minmax(0, 1fr); grid-template-areas: "pic" "verb" "facts"; grid-template-rows: auto; min-height: 0; background: var(--field-2); }
  .panel__pic { min-height: 0; aspect-ratio: 4 / 5; height: auto; }
  .panel__verb { padding: 28px var(--m) 12px; font-size: 13vw; place-items: initial; }
  .panel__facts { padding: 0 var(--m) 56px; }
}

/* Spacing and grids (Codex audit) */
.intro { padding-block: 96px clamp(96px, 9vw, 140px); }
@media (max-width: 860px) { .intro { padding: 48px var(--m) 80px; } }
.dates { margin-top: 0; padding-block: 104px; }
.dates__grid { margin-top: 48px; }
.around__grid { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 28px calc(var(--gutter) * 2); margin-top: 48px; }
.around__pic { grid-column: 1; max-width: 520px; }
.around__tables { grid-column: 2; }
.food__grid { grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 28px calc(var(--gutter) * 2); margin-top: 48px; }
.food__pics { grid-column: 1; }
.food__tables { grid-column: 2; }
@media (max-width: 860px) {
  .around__grid, .food__grid { grid-template-columns: minmax(0, 1fr); }
  .around__pic, .around__tables, .food__pics, .food__tables { grid-column: auto; }
  .trips__map { height: min(56svh, 440px); min-height: 0; }
}
.year { margin-top: 0; padding-block: 104px; gap: 48px; }
.foot { min-height: 0; grid-template-rows: auto auto auto; row-gap: 64px; padding-top: 104px; }
"""
open("css/site.css", "w", encoding="utf-8").write(css)
print("critique pass applied; not found:", missing or "none")
