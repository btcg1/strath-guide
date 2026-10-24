"""Build the Strath Field Guide: export every photo for its slot and render index.html from src/template.html.

Run from the project root:  python tools/build.py
Source photos (resized, EXIF and GPS stripped) live in _source/.
"""
import html, json, os, re
from datetime import date
from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "_source")
PH = os.path.join(ROOT, "photos")
J = lambda *p: os.path.join(ROOT, *p)
picks = json.load(open(J("data", "picks.json"), encoding="utf-8"))
trips = json.load(open(J("data", "trips.json"), encoding="utf-8"))
coords = json.load(open(J("data", "coords.json"), encoding="utf-8"))
esc = lambda s: html.escape(s, quote=True)

PLACE = {
 "skye-storr": "Old Man of Storr, Skye", "storr2": "Old Man of Storr, Skye", "skye-sligachan": "Sligachan, Skye",
 "skye-eileandonan": "Eilean Donan", "portree": "Portree, Skye", "creag": "Isle of Skye", "glenfinnan": "Glenfinnan Viaduct",
 "glenfinnan-view": "On the road to Glenfinnan", "luss": "Luss, Loch Lomond", "oban": "Oban", "kilchurn": "Kilchurn Castle, Loch Awe",
 "inveraray": "Inveraray", "restbe": "Rest and Be Thankful", "glencoe": "Glencoe", "lochness": "Urquhart Castle, Loch Ness",
 "fortaugustus": "Fort Augustus", "inverness": "Inverness", "falkirk": "The Kelpies, Falkirk", "inchcolm": "Inchcolm Abbey",
 "queensferry": "Forth Bridge, South Queensferry", "inchcolm-boat": "Firth of Forth", "arbroath": "Arbroath",
 "arbroath-docks": "Arbroath harbour", "hamilton": "Hamilton Park races", "stirling": "Stirling", "wallace": "Stirling, from the Wallace Monument",
 "culross": "Culross", "dunnottar": "Dunnottar Castle", "stonehaven": "Stonehaven", "standrews": "St Andrews",
 "standrews-beach": "St Andrews beach", "oldcourse": "The Old Course, St Andrews", "arran": "Isle of Arran", "newlanark": "New Lanark",
 "lanark": "Lanark", "edinburgh": "Edinburgh", "arthurseat": "Arthur's Seat, Edinburgh", "edi-market": "Edinburgh",
 "edi-museum": "Edinburgh", "lomond": "Loch Lomond", "hillhouse": "The Hill House, Helensburgh", "footdee": "Footdee, Aberdeen",
 "aberdeen-beach": "Aberdeen beach", "aber-uni": "University of Aberdeen", "aber-city": "Aberdeen", "crathes": "Crathes Castle",
 "alford": "Alford", "prestonmill": "Preston Mill, East Linton", "eastlinton": "East Linton", "tantallon": "Tantallon Castle",
 "northberwick": "North Berwick", "argyll": "Argyll Forest", "dunoon": "Dunoon", "dunkeld": "Dunkeld", "causeway": "Giant's Causeway",
 "belfast": "Belfast", "derry": "Derry", "aviemore": "Rothiemurchus, Aviemore", "wick": "Wick", "culloden": "Culloden",
 "chester": "Chester", "conwy": "Conwy", "llandudno": "Llandudno", "snowdonia": "Snowdonia", "shrewsbury": "Shrewsbury",
 "manchester": "Manchester", "york": "York", "york-rail": "National Railway Museum, York", "gla-necropolis": "Glasgow Necropolis",
 "gla-cathedral": "Glasgow Cathedral", "gla-strath": "University of Strathclyde", "gla-uog": "University of Glasgow",
 "gla-city": "Glasgow", "gla-pollok": "Pollok Park, Glasgow", "pollok-art": "Burrell Collection, Glasgow",
 "gla-kelvingrove": "Kelvingrove, Glasgow", "gla-riverside": "Riverside Museum, Glasgow", "gla-barras": "Barras Market, Glasgow",
}
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def nice_date(iso):
    d = date.fromisoformat(iso); return f"{d.day} {MONTHS[d.month-1]}"
folder_trip = {f: t for t in trips for f in t["folders"]}
def caption(key):
    sheet = key.rsplit("_", 1)[0]
    name = PLACE.get(sheet, sheet.replace("-", " ").title())
    t = folder_trip.get(sheet)
    return f"{name}, {nice_date(t['date'])}" if t else name

def crop(im, ratio, y=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = (w - nw) // 2; return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); top = max(0, min(h - nh, int(h * y - nh / 2))); return im.crop((0, top, w, top + nh))

def export(key, rel, ratio=None, size=(800, 1000), y=0.5, q=80, dark=None):
    out = J("photos", rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out):
        im = Image.open(os.path.join(FULL, key + ".jpg")).convert("RGB")
        if ratio: im = crop(im, ratio, y)
        im.thumbnail(size, Image.LANCZOS)
        if dark: im = ImageEnhance.Brightness(im).enhance(dark)
        im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
    w, h = Image.open(out).size
    return "photos/" + rel.replace("\\", "/"), w, h

large_cache = {}
def large(key):
    if key not in large_cache:
        large_cache[key] = export(key, f"large/{key}.jpg", None, (1200, 1800), q=78)[0]
    return large_cache[key]

def img(src, w, h, alt="", cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img{c} src="{src}" alt="{esc(alt)}" width="{w}" height="{h}"{l}{extra}>'

R = {}
# Hero strip
strips = []
for i, s in enumerate(picks["strip"]):
    wsrc, ww, wh = export(s["file"], f"strip/{i}-w.jpg", 5.0, (1600, 320), s["y"])
    msrc, mw, mh = export(s["file"], f"strip/{i}-m.jpg", 2.0, (1000, 500), s["y"])
    on = ' is-on' if i == 0 else ''
    strips.append(f'<img class="{on.strip()}" src="{wsrc}" data-mobile="{msrc}" data-cap="{esc(s["cap"])}" alt="{esc(s["cap"])}" width="{ww}" height="{wh}"{"" if i == 0 else " loading=\"lazy\""}>')
R["STRIP_IMGS"] = "\n          ".join(strips)
R["STRIP0"] = "photos/strip/0-w.jpg"
R["STRIP_CAPTION0"] = esc(picks["strip"][0]["cap"])
L = json.load(open(J("data", "links.json"), encoding="utf-8"))
A = lambda key, text: f'<a href="{L[key]}">{text}</a>'
gstr = []
for i, s_ in enumerate(picks["gstrip"]):
    wsrc, ww, wh = export(s_["file"], f"gstrip/{i}-w.jpg", 5.0, (1600, 320), s_["y"])
    msrc, mw, mh = export(s_["file"], f"gstrip/{i}-m.jpg", 2.0, (1000, 500), s_["y"])
    gstr.append(f'<img class="{"is-on" if i == 0 else ""}" src="{wsrc}" data-mobile="{msrc}" data-cap="{esc(s_["cap"])}" alt="{esc(s_["cap"])}" width="{ww}" height="{wh}"{"" if i == 0 else " loading=\"lazy\""}>')
R["G_STRIP_IMGS"] = "\n          ".join(gstr)
R["G_STRIP0"] = "photos/gstrip/0-w.jpg"
export(picks["gstrip"][0]["file"], "og/guide.jpg", 1200 / 630, (1200, 630), picks["gstrip"][0]["y"])
export(picks["strip"][0]["file"], "og/travel.jpg", 1200 / 630, (1200, 630), picks["strip"][0]["y"])
R["G_STRIP_CAPTION0"] = esc(picks["gstrip"][0]["cap"])
def strip(name, items):
    """Hero strip for the Food and Shopping tabs, plus that page's link-preview image."""
    out = []
    for i, s_ in enumerate(items):
        wsrc, ww, wh = export(s_["file"], f"{name}/{i}-w.jpg", 5.0, (1600, 320), s_["y"])
        msrc, mw, mh = export(s_["file"], f"{name}/{i}-m.jpg", 2.0, (1000, 500), s_["y"])
        out.append(f'<img class="{"is-on" if i == 0 else ""}" src="{wsrc}" data-mobile="{msrc}" data-cap="{esc(s_["cap"])}" alt="{esc(s_["cap"])}" width="{ww}" height="{wh}"{"" if i == 0 else " loading=\"lazy\""}>')
    export(items[0]["file"], f"og/{name}.jpg", 1200 / 630, (1200, 630), items[0]["y"])
    return "\n          ".join(out), f"photos/{name}/0-w.jpg", esc(items[0]["cap"])
R["F_STRIP_IMGS"], R["F_STRIP0"], R["F_STRIP_CAPTION0"] = strip("fstrip", picks["fstrip"])
R["S_STRIP_IMGS"], R["S_STRIP0"], R["S_STRIP_CAPTION0"] = strip("sstrip", picks["sstrip"])
for k, key in {"APPLY": "gla-strath_2", "MATCH": "gla-uog_2", "FLY": "glenfinnan_0", "SETTLE": "gla-city_1"}.items():
    R["GI_" + k] = export(key, f"intro/g-{k.lower()}.jpg", 4 / 3, (300, 225))[0]

# Intro thumbs
for k, key in picks["intro"].items():
    src, w, h = export(key, f"intro/{k}-p.jpg", 4 / 5, (640, 800))
    R["INTRO_" + k.upper()] = src

# Trips: fallback list (visible without JS) and the data the map uses
lis, tj = [], []
for t in trips:
    keys = picks["trips"][t["id"]]
    pics, pj = [], []
    for k, key in enumerate(keys):
        src, w, h = export(key, f"trips/{t['id']}-{k}.jpg", 4 / 5, (640, 800))
        pics.append(img(src, w, h, caption(key), extra=f' data-large="{large(key)}"'))
        pj.append({"src": src, "large": large(key), "cap": caption(key)})
    when = nice_date(t["date"]) + (f" – {nice_date(t['end'])}" if t["end"] else "")
    lis.append(f'<li class="trip-card" data-id="{t["id"]}"><div class="trip-card__pics">{"".join(pics)}</div>'
               f'<p class="trip-card__name">{esc(t["name"])}</p>'
               f'<p class="trip-card__meta">{when} 2025. {esc(t["how"])}.</p><p>{esc(t["line"])}</p></li>')
    tj.append({**{k: t[k] for k in ("id", "name", "date", "end", "how", "line", "pins")}, "when": when, "pics": pj})
R["TRIP_FALLBACK"] = "\n        ".join(lis)
R["TRIPS_JSON"] = json.dumps(tj, ensure_ascii=False)
R["COORDS_JSON"] = json.dumps({k: [v["lat"], v["lon"]] for k, v in coords.items()})

# Map: our own SVG outline (no tiles), pins for every trip, a few towns for orientation
M = json.load(open(J("data", "map.json"), encoding="utf-8"))
R["MAPPROJ"] = json.dumps({"lon0": M["lon0"], "lat0": M["lat0"], "k": M["k"]})
def pxy(key):
    lat, lon = coords[key]["lat"], coords[key]["lon"]
    return (lon - M["lon0"]) * M["k"] * 100, -(lat - M["lat0"]) * 100
allp = [pxy(p) for t in trips for p in t["pins"] if p in coords] + [pxy("strath")]
xs, ys = [p[0] for p in allp], [p[1] for p in allp]
vx, vy, vw, vh = min(xs) - 40, min(ys) - 40, max(xs) - min(xs) + 80, max(ys) - min(ys) + 80
pins = []
for i, t in enumerate(trips):
    for p in t["pins"]:
        if p in coords:
            x, y = pxy(p)
            pins.append(f'<circle class="mpin" data-i="{i}" cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{esc(t["name"])}</title></circle>')
TOWNS = [("Glasgow", "strath", -1), ("Edinburgh", "edinburgh", 1), ("Aberdeen", "aberdeen", 1), ("Inverness", "inverness", 1), ("Belfast", "belfast", 1)]
towns = "".join(f'<text class="mtown" x="{pxy(k)[0] + 6 * d:.1f}" y="{pxy(k)[1] + 14:.1f}" text-anchor="{"end" if d < 0 else "start"}">{n}</text>' for n, k, d in TOWNS)
hx, hy = pxy("strath")
R["MAP_SVG"] = (f'<svg class="map" id="map" viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Map of the 24 trips from Glasgow">'
                f'<g class="mland">{"".join(f"<path d=\"{d}\"/>" for d in M["paths"])}</g>'
                f'<g class="mtowns">{towns}</g><path class="mroute" d=""/>'
                f'<g class="mpins">{"".join(pins)}</g>'
                f'<rect class="mhome" x="{hx - 4:.1f}" y="{hy - 4:.1f}" width="8" height="8"><title>University of Strathclyde</title></rect>'
                f'<text class="mlabel" x="0" y="0"></text></svg>')

# Verb panels
VERBS = [
 ("apply", "Apply", f"<p>You apply through NTU's {A('gem_explorer', 'GEM Explorer')} on the {A('gem_portal', 'GEM Mobility Portal')}. You need to have finished two NTU semesters, have a CGPA of 3.3 or above, and not have been on an in-person exchange before. You rank three universities, and NTU allocates places by CGPA band, citizenship, your ranking and how many spots each school has.</p><ul><li>{A('strath_partners', 'Strathclyde takes nominations')} <span class='n'>1 March – 15 May</span> for a September start and <span class='n'>15 September – 15 October</span> for January. NTU sends your nomination. Then keep an eye out for Strath's email.</li><li>Then you apply to Strath online with your passport, NTU transcript and class choices.</li></ul>"),
 ("match", "Match courses", f"<p>Course matching is the part everyone panics about. Find past matches in {A('coursefinder', 'CourseFinder')}, then submit each one in NTU's {A('coursematching', 'online course matching system')} (both need your NTU login).</p><ul><li>Pick from Strath's {A('strath_classes', 'exchange class catalogue')} and check for timetable clashes yourself.</li><li>Officially Strath allows classes from at most two departments. Honestly, don't stress too much. Strath's coordinators know NTU course matching can be a headache, and they're flexible as long as most of your classes are in your primary department. One of us (MAE) had MAE, EEE and DMEM classes approved; <a href='#mae'>the full list is below</a>.</li><li>Exchange grades count towards your AUs, not your CGPA.</li></ul>"),
 ("fly", "Before you fly", f"<p>Get a {A('eta', 'UK ETA')} before you fly: £20 on GOV.UK or the UK ETA app. It usually comes through within a day, but give it 3 working days. It lasts 2 years.</p><ul><li>You enter as a {A('visit_study', 'Standard Visitor')}, which lets you study for up to 6 months but not work, not even an unpaid internship.</li><li>Before you leave, do NTU's briefing, indemnity letter, ISOS app and {A('ntu_predep', 'Travel Registry')} declaration, and {A('mfa_eregister', 'eRegister with MFA')} for the trip.</li><li>At the border, carry your acceptance letter, accommodation details and proof of funds. Keep your boarding pass afterwards too.</li></ul>"),
 ("settle", "Settle in", f"<p>From the airport, take the {A('airport500', 'Airport Express 500')}. It runs every 10 minutes, 24 hours a day, to Buchanan Bus Station, about a 15-minute walk from the halls. Collect your keys at Lord Todd. After you collect your keys, check the free market of cutlery, plates, decor and storage left by past students. Take what you need.</p><ul><li>Week one: a {A('lebara', 'UK SIM')}, a {A('railcard1625', 'Railcard')}, {A('monzo', 'Monzo')}, and the {A('esncard', 'ESNcard')} at the society fair. Get it early: it sold out last time and wasn't restocked until the end of the semester.</li><li>Then head to TJ Hughes in the St Enoch Centre for bedding, pans and a laundry basket. Split an Uber back four ways and it's cheap.</li><li>Go to every class in week 1. Every lecturer takes attendance differently: QR code, password or paper.</li></ul>"),
]
panels = []
for vid, word, facts in VERBS:
    key = picks["verbs"][vid]
    d, dw, dh = export(key, f"verbs/{vid}-p.jpg", 4 / 5, (1066, 1333))
    panels.append(f'<article class="panel" id="step-{vid}" aria-label="{word}"><figure class="panel__pic">'
                  f'{img(d, dw, dh, caption(key))}</figure><h2 class="panel__verb">{word}</h2><div class="panel__facts">{facts}</div></article>')
R["VERB_PANELS"] = "\n  ".join(panels).replace("<picture>", "<picture>", 1)

# Getting-around picture
src, w, h = export(picks["intro"]["street"], "around/glasgow.jpg", 4 / 5, (800, 1000))
R["AROUND_PIC"], R["AROUND_ALT"] = src, caption(picks["intro"]["street"])  # template sets loading on this one

# Places index: name, how, when, cost, photo key
P = [
 ("Weekend tours", "ESN Strathclyde's weekend tours cost about £45 and pick you up from campus. Last year's code was ESN25.", [
  ("Isle of Skye", "ESN or Rabbies weekend tour", "Year-round. Eilean Donan is shut all January", "Hostels up to £70 a bed", "skye-sligachan_5"),
  ("Glencoe", "Ember coach from Buchanan", "Year-round", "Free to walk", "glencoe_2"),
  ("Glenfinnan", "ESN day tour or ScotRail", "Viewpoint daily. Steam train April–October", "Viewpoint free. Steam train £76 return", "glenfinnan_6"),
  ("Loch Ness", "ESN day tour", "Urquhart Castle 9:30–16:30 in winter", "£1 with Young Scot or NEC. Book parking", "lochness_7")]),
 ("By train", "ScotRail has no peak fares. A Railcard takes a third off.", [
  ("Dunkeld & Birnam", "Queen Street", "The Hermitage, daily", "Free", "dunkeld_1"),
  ("Aviemore & Rothiemurchus", "Queen Street", "Year-round", "Pay for activities separately", "aviemore_4"),
  ("Oban", "Queen Street", "Staffa boats April–October", "", "oban_2"),
  ("Loch Lomond & Hill House", "To Balloch, then Helensburgh", "Year-round", "Free to visit the loch", "lomond_5"),
  ("Stirling", "Queen Street", "Castle 9:30–17:00 Oct–Mar, to 18:00 Apr–Sep", "Castle £1 with Young Scot or NEC", "wallace_3"),
  ("Falkirk", "Queen Street", "Wheel 9:45–17:30 daily", "Boat from £14.63, students £13.20", "falkirk_4"),
  ("Arbroath", "Queen Street", "Year-round", "Free", "arbroath_3"),
  ("New Lanark", "Central to Lanark", "Year-round", "£15.50, concession £11.50", "newlanark_3"),
  ("Aberdeen", "Queen Street", "Year-round", "Free to explore", "footdee_3"),
  ("Dunnottar Castle", "Train to Stonehaven", "Shorter hours in winter", "£13.50, students £12", "dunnottar_8"),
  ("East Linton & Preston Mill", "Train to East Linton", "Mill shut 20 Dec – 28 Feb", "£11, concession £9", "prestonmill_1"),
  ("Linlithgow", "Queen Street", "Palace year-round", "£1 with Young Scot or NEC", None),
  ("Thurso & Wick", "Via Inverness", "Year-round", "", "wick_4")]),
 ("By ferry", "Most island boats run spring to autumn. Check the calendar first.", [
  ("Isle of Arran", "Central to Ardrossan (55 min crossing) or Troon (80 min)", "Year-round", "", "arran_1"),
  ("Inchcolm Island", "Train, then Maid of the Forth", "Abbey open April–October", "Boat £29.50 + abbey £8.50", "inchcolm_0"),
  ("Puffins & North Berwick", "Scottish Seabird Centre boats", "Late March – early October", "Catamaran £32", "northberwick_3"),
  ("Isle of May", "May Princess from Anstruther", "Seasonal", "£40, students £35", None),
  ("Shetland", "NorthLink overnight from Aberdeen", "Year-round", "From £29.50 one way", None)]),
 ("By bus", "The Stagecoach East Scotland DayRider is £12.80 for a day.", [
  ("St Andrews", "Direct bus from Buchanan", "Sundays: Old Course open to walkers", "Castle £1 with Young Scot or NEC", "standrews_3"),
  ("Culross", "Stagecoach", "Palace shut Nov–Mar", "Palace £14, concession £11", "culross_5"),
  ("Anstruther & Fife Coastal Path", "Stagecoach, one change", "Year-round", "DayRider £12.80", None),
  ("Hamilton Park", "Train from Central", "Race days", "", "hamilton_1")]),
 ("By coach", "Flixbus is usually the cheapest. Student Beans gets you 20% off.", [
  ("Edinburgh", "Flixbus or train", "Castle 9:30–18:00 Apr–Sep", "Castle £23.50 online", "edinburgh_0"),
  ("Giant's Causeway & Belfast", "Citylink/Ulsterbus 923 via Cairnryan", "Year-round", "From £37 advance single", "causeway_6"),
  ("York", "Train from Central", "Year-round", "", "york_1"),
  ("Chester & North Wales", "Train from Central", "Year-round", "", "snowdonia_5")]),
 ("In Glasgow", "Most of the big museums are free.", [
  ("West End & Kelvingrove", "Subway from Buchanan Street", "Organ recital 1pm Mon–Sat, 3pm Sun", "Free", "gla-uog_1"),
  ("Cathedral & Necropolis", "Walk from campus", "Necropolis 7:00–16:30 daily", "Free. Book a cathedral slot", "gla-necropolis_4"),
  ("Pollok Park & the Burrell", "Train or bus", "Museum opens at 10:00 or 11:00", "Free", "gla-pollok_5"),
  ("Hunterian Museum", "Subway to Hillhead", "Tue–Sun 10:00–17:00", "Free", None),
  ("City Chambers", "Walk", "Tours Mon–Fri 10:30 and 14:30", "Free", None),
  ("Tennent's Brewery", "Walk", "1.5-hour tours", "From £17, 18+", None)]),
]
PLACE_NOTE = {'Isle of Skye': "Easily the most scenic hike we did (Old Man of Storr), but you need luck with the weather or you'll get blown off the mountain.", 'Glencoe': "Getting to Glencoe is annoying, but honestly, go.", 'Glenfinnan': "The Harry Potter viaduct. One of the ESN tours we'd recommend.", 'Dunkeld & Birnam': "One of our favourite places in Scotland. On a good weather day it's so scenic, very reconnect-with-nature vibes.", 'Aviemore & Rothiemurchus': 'Highly recommend. Outdoor heaven: trails, quad bikes, ziplining, horse riding.', 'Stirling': 'Very hilly, so give yourself time. If you pay for the castle, follow the free guided tour.', 'Falkirk': 'A very therapeutic walk along the canal from the Wheel to the Kelpies.', 'New Lanark': "The mill village feels surreal, and the walk down from the station is steep.", 'East Linton & Preston Mill': "Farmers' markets, proper village vibes and a bakery that feels surprisingly modern.", 'Thurso & Wick': 'If you like remote, peaceful places, the coastal walk is lovely.', 'Isle of Arran': 'Absolutely beautiful, and close to school. We can’t recommend it enough.', 'Inchcolm Island': 'An abandoned abbey on an uninhabited island. Queensferry, where the boat leaves, is a beautiful seaside town.', 'Puffins & North Berwick': 'Book fast when tickets drop: the cheap Puffin Express sold out in a day. We saw so many puffins, and seals too.', 'St Andrews': 'Go on a Sunday, when the Old Course opens to the public. Cheesy Toast Shack and Jannettas Gelateria are so good.', 'Culross': 'A small town that looks like the Italian countryside.', 'Edinburgh': "Calton Hill is a nice place to chill, and there's a café. Bertie's might be the best fish and chips in Scotland.", 'Cathedral & Necropolis': 'Walkable from school, and great at golden hour.', 'Pollok Park & the Burrell': 'Highland cows up close, and a free art museum.'}
PLACE_LINK = {'Glencoe': 'ember', 'Glenfinnan': 'glenfinnan', 'Loch Ness': 'urquhart', 'Dunkeld & Birnam': 'hermitage', 'Oban': 'staffa', 'Stirling': 'stirling_castle', 'Falkirk': 'falkirk_wheel', 'New Lanark': 'newlanark', 'Dunnottar Castle': 'dunnottar', 'East Linton & Preston Mill': 'prestonmill', 'Linlithgow': 'linlithgow', 'Isle of Arran': 'calmac_arran', 'Inchcolm Island': 'maidoftheforth', 'Puffins & North Berwick': 'seabird', 'Isle of May': 'isleofmay', 'Shetland': 'northlink', 'St Andrews': 'standrews_castle', 'Culross': 'culross', 'Anstruther & Fife Coastal Path': 'dayrider', 'Edinburgh': 'edinburgh_castle', "Giant's Causeway & Belfast": 'belfast923', 'West End & Kelvingrove': 'kelvingrove', 'Cathedral & Necropolis': 'necropolis', 'Pollok Park & the Burrell': 'burrell', 'Hunterian Museum': 'hunterian', 'City Chambers': 'citychambers', "Tennent's Brewery": 'tennents'}
NOTE = {'Weekend tours': lambda t: t.replace('ESN Strathclyde', A('esn_strath', 'ESN Strathclyde')), 'By train': lambda t: t.replace('ScotRail', A('scotrail', 'ScotRail')).replace('A Railcard', 'A ' + A('railcard1625', 'Railcard')), 'By bus': lambda t: t.replace('Stagecoach East Scotland DayRider', A('dayrider', 'Stagecoach East Scotland DayRider')), 'By coach': lambda t: t.replace('Flixbus', A('flixbus', 'Flixbus')).replace('Student Beans', A('flix_sb', 'Student Beans'))}
groups, count = [], 0
for title, note, rows in P:
    lis = []
    for name, how, when, cost, key in rows:
        count += 1
        if key:
            src, w, h = export(key, f"places/{key}.jpg", 4 / 5, (600, 750), 0.62)
            thumb = img(src, w, h, cls="index__thumb")
            prev = f' data-preview="{src}" data-name="{esc(name)}"'
        else:
            thumb, prev = '', ' data-nothumb'
        info = f'<span>{esc(how)}</span><span>{esc(when)}</span><span>{esc(cost)}</span>'
        nm = f'<a class="index__name" href="{L[PLACE_LINK[name]]}">{esc(name)}</a>' if name in PLACE_LINK else f'<span class="index__name">{esc(name)}</span>'
        ti = '' if name in PLACE_LINK else ' tabindex="0"'
        nt = f'<span class="index__note">{esc(PLACE_NOTE[name])}</span>' if name in PLACE_NOTE else ''
        lis.append(f'<li class="index__row"{ti}{prev}>{thumb}{nm}<span class="index__info">{info}</span>{nt}</li>')
    groups.append(f'<div class="index__group"><h3>{esc(title)}</h3><p>{NOTE.get(title, lambda t: t)(esc(note))}</p><ul class="index__list">{"".join(lis)}</ul></div>')
R["PLACES"] = "\n    ".join(groups)
first = P[0][2][0]
R["PLACE0"] = export(first[4], f"places/{first[4]}.jpg", 4 / 5, (600, 750), 0.62)[0]
R["PLACE0_NAME"] = esc(first[0])
for k, key, y in [("TRIPS", "skye-storr_4", 0.62), ("YEAR", "inchcolm_0", 0.62), ("PLACES", "glenfinnan_0", 0.74)]:
    R["HS_" + k] = export(key, f"hstrip/{k.lower()}.jpg", 3.0, (600, 200), y)[0]

# Prints over the "Camera roll" headline
prints = []
for i, p in enumerate(picks["prints"]):
    src, w, h = export(p["file"], f"prints/{i}.jpg", 3 / 4, (700, 933))
    prints.append(f'<figure class="print print--{"abc"[i]}" data-large="{large(p["file"])}">{img(src, w, h, p["cap"], lazy=False)}</figure>')
R["PRINTS"] = "\n    ".join(prints)

# Album: the photo wall grouped by trip, in date order, Glasgow first (data/album.json holds the curated keys)
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
    blocks.append(f'<div class="album__group"><div class="album__head"><h3 class="album__title">{esc(title)}</h3><p class="album__when">{esc(when)}</p></div><div class="album__grid">{"".join(figs)}</div></div>')
R["WALL"] = "\n    ".join(blocks)
R["WALL_COUNT"] = str(len(order))

# Food photos: three by the "where we ate" tables, four on the Scottish menu (no repeats)
food = {f["file"]: f["caption"] for f in picks["food"]}
fp = []
for i, key in enumerate(["aviemore_0", "oban_1", "arran_3"]):
    src, w, h = export(key, f"food/eat-{i}.jpg", 4 / 5, (700, 875))
    fp.append(f'<figure data-large="{large(key)}">{img(src, w, h, food[key], lazy=False)}<figcaption>{esc(food[key])}</figcaption></figure>')
R["FOOD_PICS"] = "".join(fp)
for k, key in {"HAGGIS": "gla-city_8", "FISH": "portree_0", "STP": "food_4", "ROAST": "arbroath-docks_6"}.items():
    R["SCOT_" + k] = export(key, f"food/scot-{k.lower()}.jpg", 4 / 5, (640, 800))[0]
    R["SCOT_" + k + "_L"] = large(key)

# Shopping tab section photos (album shots reused: every vendored photo is already placed somewhere)
for k, key in {"HALLS": "gla-cathedral_4", "GEAR": "glencoe_1"}.items():
    R["SHOP_PIC_" + k] = export(key, f"shop/{k.lower()}.jpg", 4 / 5, (640, 800))[0]
    R["SHOP_PIC_" + k + "_L"] = large(key)

# Meal deal dot plot (Student Beans, 11 August 2026): standard price, and loyalty-card price where there is one
DEALS = [("Asda", 3.74, None, None), ("Sainsbury's", 3.95, None, None), ("Boots", 3.99, 3.60, "an Advantage Card"),
         ("Morrisons", 4.00, 3.75, "My Morrisons"), ("Co-op", 4.10, 3.75, "Co-op membership"), ("Tesco", 4.25, 3.85, "a Clubcard")]
x = lambda v: f"{(v - 3.5) / 1.0 * 100:.1f}%"
rows = []
for name, std, card, scheme in DEALS:
    dots = f'<i class="dots__std" style="--x:{x(std)}"></i>' + (f'<i class="dots__card" style="--x:{x(card)}"></i>' if card else "")
    text = f"£{std:.2f}" + (f", or £{card:.2f} with {scheme}" if card else "")
    rows.append(f'<li class="dots__row"><span class="dots__name">{esc(name)}</span><span class="dots__track" aria-hidden="true">{dots}</span><span class="dots__text">{esc(text)}</span></li>')
rows.append('<li class="dots__axis" aria-hidden="true"><span></span><span class="dots__track"><b style="--x:0%">£3.50</b><b style="--x:50%">£4.00</b><b style="--x:100%">£4.50</b></span><span></span></li>')
R["MEALDEAL_ROWS"] = "\n    ".join(rows)

# Sources
S = [
 ("NTU", [("GEM Explorer exchange programmes", "https://www.ntu.edu.sg/education/student-exchanges/exchange-programmes"),
          ("GEM Explorer process chart (PDF)", "https://www.ntu.edu.sg/media/docs/librariesprovider143/undergraduate/gem-explorer-process-flow_20260324.pdf?sfvrsn=89208a65_1"),
          ("Course matching and credit transfer (PDF)", "https://www.ntu.edu.sg/docs/librariesprovider143/default-document-library/course-matching-credit-transfer-guidelines_260324.pdf?sfvrsn=80f11d8d_1"),
          ("Pre-departure requirements", "https://www.ntu.edu.sg/education/student-exchanges/important-information/travel-safety-and-security/pre-departure-requirements"),
          ("Student travel insurance", "https://www.ntu.edu.sg/life-at-ntu/student-life/student-services/onestop/insurance-coverage/student-travel-insurance")]),
 ("University of Strathclyde", [("Nominations (information for partners)", "https://www.strath.ac.uk/studywithus/studyabroad/comingtostrathclyde/informationforpartners/"),
          ("Exchange factsheet 2026/27 (PDF)", "https://www.strath.ac.uk/media/1newwebsite/studyabroad/documents/Factsheet_2026-2027.pdf"),
          ("Key dates 2026/27", "https://www.strath.ac.uk/keydates/2026-27/"),
          ("Accommodation for exchange students", "https://www.strath.ac.uk/studywithus/accommodation/exchangestudents/"),
          ("Accommodation FAQs", "https://www.strath.ac.uk/studywithus/accommodation/faqs/"),
          ("Exam timetable FAQs", "https://www.strath.ac.uk/professionalservices/studentexperience/studentlifecycle/exams/examtimetablefaqs/")]),
 ("Entry, health, weather", [("GOV.UK: apply for an ETA", "https://www.gov.uk/eta/apply"), ("GOV.UK: visit to study", "https://www.gov.uk/standard-visitor/visit-to-study"),
          ("NHS inform: overseas visitors", "https://www.nhsinform.scot/care-support-and-rights/health-rights/access/healthcare-for-overseas-visitors/"),
          ("Met Office: Glasgow averages", "https://www.metoffice.gov.uk/research/climate/maps-and-data/location-specific-long-term-averages/gcuvzv5wy")]),
 ("Transport", [("Glasgow Airport Express 500", "https://www.glasgowairport.com/to-and-from/glasgow-airport-express-service-500/"),
          ("16–25 Railcard", "https://www.railcard.co.uk/16-25-railcard/"), ("26–30 Railcard", "https://www.railcard.co.uk/26-30-railcard/"),
          ("ScotRail peak fares removal", "https://www.transport.gov.scot/publication/scotrail-peak-fares-permanent-removal-outline-business-case/summary-conclusion-and-recommendation/"),
          ("Under-22s free bus travel", "https://www.transport.gov.scot/concessionary-travel/under-22s-free-bus-travel"),
          ("Stagecoach East Scotland DayRider", "https://www.stagecoachbus.com/promos-and-offers/east-scotland/go-to-glasgow-by-bus"),
          ("Ember", "https://www.ember.to/news/"), ("Coach and sail to Belfast (923)", "https://www.stenaline.co.uk/coach-and-sail/to-ireland-ulsterbus"),
          ("CalMac: Arran", "https://www.calmac.co.uk/en-gb/destinations/arran/"), ("NorthLink 2027 fares", "https://www.northlinkferries.co.uk/book/routes-times-and-prices/2027-fares/")]),
 ("Money and deals", [("NTS membership", "https://www.nts.org.uk/join"), ("NTS membership terms", "https://www.nts.org.uk/terms-conditions/membership-terms-conditions"),
          ("HES visitor FAQs (student and Young Scot prices)", "https://www.historicenvironment.scot/visit/visitor-faqs/"), ("ESNcard × Ryanair", "https://www.esncard.org/ryanair"),
          ("Student Beans: Flixbus", "https://www.studentbeans.com/student-discount/uk/flixbus"), ("Student Beans: Greggs", "https://www.studentbeans.com/student-discount/uk/greggs"),
          ("Tesco meal deals", "https://www.tesco.com/shop/en-GB/browse/groceries-and-essentials/fresh-food/chilled-soup-sandwiches-and-salad-pots/lunch-meal-deals"),
          ("Lebara SIM plans", "https://www.lebara.co.uk/en/best-sim-only-deals.html"), ("VOXI roaming", "https://www.voxi.co.uk/help/roaming-international/does-voxi-have-european-roaming"),
          ("Exchange rate (open.er-api.com)", "https://open.er-api.com/v6/latest/GBP")]),
 ("Food and shopping", [("First Bus £2 fare cap", "https://www.firstbus.co.uk/greater-glasgow/tickets/ps2-fare-cap"),
          ("Subway contactless fares", "https://www.spt.co.uk/tickets/subway-tickets/subway-contactless-help/"),
          ("Meal deal prices (Student Beans, Aug 2026)", "https://www.studentbeans.com/blog/uk/best-supermarket-meal-deals-in-the-uk"),
          ("Student Beans: Wagamama", "https://www.studentbeans.com/student-discount/uk/wagamama"),
          ("Too Good To Go", "https://www.toogoodtogo.com/en-gb"), ("Co-op membership", "https://www.coop.co.uk/membership"),
          ("Lidl Plus", "https://www.lidl.co.uk/c/lidl-plus/s10023095"), ("Nectar Prices", "https://www.nectar.com/nectar-prices"),
          ("Carrier bag charge", "https://www.mygov.scot/carrier-bag-charge"), ("Minimum unit pricing", "https://www.mygov.scot/minimum-unit-price-alcohol"),
          ("Sunday trading (GOV.UK)", "https://www.gov.uk/trading-hours-for-retailers-the-law"), ("The Barras opening times", "https://market.barrowland.co.uk/blogs/the-barras/opening-times"),
          ("TJ Hughes, St Enoch", "https://st-enoch.com/directory/tj-hughes"), ("Uniqlo, St Enoch", "https://st-enoch.com/directory/uniqlo"),
          ("StrathApp", "https://www.strath.ac.uk/studywithus/mobileapp/"), ("Strathclyde Sport for halls residents", "https://www.strath.ac.uk/studywithus/accommodation/strathclydesport/"),
          ("Exchange class catalogue: Mechanical & Aerospace", "https://www.strath.ac.uk/studywithus/studyabroad/comingtostrathclyde/academicinformation/exchangeclasscatalogue/mechanicalaerospaceengineering/"),
          ("Exchange class catalogue: Electronic & Electrical", "https://www.strath.ac.uk/studywithus/studyabroad/comingtostrathclyde/academicinformation/exchangeclasscatalogue/electronicelectricalengineering/")]),
 ("Places", [("Kelvingrove organ recital", "https://www.glasgowlife.org.uk/museums/venues/kelvingrove-art-gallery-and-museum/top-ten-must-see"),
          ("Hunterian", "https://www.gla.ac.uk/hunterian/visit/our-venues/"), ("Glasgow Necropolis", "https://www.glasgownecropolis.org/about-glasgow-necropolis/location-faqs/"),
          ("City Chambers tours", "https://www.glasgow.gov.uk/article/1066/City-Chambers-Tour"), ("Tennent's tours", "https://www.tennents.com/uk/experience/tours"),
          ("Edinburgh Castle", "https://www.edinburghcastle.scot/plan-your-visit/tickets/"), ("Stirling Castle", "https://www.historicenvironment.scot/visit/all/stirling-castle/plan-your-visit/"),
          ("Urquhart Castle", "https://www.historicenvironment.scot/visit/all/urquhart-castle/plan-your-visit/"),
          ("Falkirk Wheel", "https://www.scottishcanals.co.uk/visit/canals/visit-the-forth-clyde-canal/attractions/the-falkirk-wheel"),
          ("New Lanark", "https://newlanark.org/your-visit/opening-times-prices/"), ("Culross Palace", "https://www.nts.org.uk/visit/places/culross/planning-your-visit"),
          ("Preston Mill", "https://www.nts.org.uk/visit/places/preston-mill/planning-your-visit"), ("Glenfinnan", "https://www.nts.org.uk/visit/places/glenfinnan-monument/planning-your-visit"),
          ("The Hermitage", "https://www.nts.org.uk/visit/places/the-hermitage/planning-your-visit"), ("Jacobite steam train", "https://westcoastrailways.co.uk/jacobite/fare-prices"),
          ("Dunnottar Castle", "https://www.dunnottarcastle.co.uk/book-now"), ("Eilean Donan", "https://www.eileandonancastle.com/visit/opening-hours/"),
          ("Inchcolm Abbey", "https://www.historicenvironment.scot/visit/all/inchcolm-abbey/plan-your-visit/"), ("Maid of the Forth", "https://www.maidoftheforth.co.uk/further-information"),
          ("Scottish Seabird Centre boats", "https://www.seabird.org/boats/"), ("May Princess", "https://www.anstrutherpleasurecruises.co.uk/info.php"),
          ("Staffa Tours", "https://staffatours.com/faq/")]),
]
R["SOURCES"] = "".join(f'<div><b>{esc(g)}</b>{"".join(f"<a href=\"{u}\">{esc(t)}</a>" for t, u in links)}</div>' for g, links in S)

for src_name, out_name in (("guide.html", "index.html"), ("food.html", "food.html"), ("shopping.html", "shopping.html"), ("travel.html", "travel.html")):
    page = open(J("src", src_name), encoding="utf-8").read()
    for k, v in R.items():
        page = page.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not left, (src_name, left)
    open(J(out_name), "w", encoding="utf-8").write(page)
n = sum(len(fs) for _, _, fs in os.walk(PH))
mb = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(PH) for f in fs) / 1e6
print(f"index.html + travel.html written. {count} places, {len(order)} wall photos, {n} image files, {mb:.1f} MB")
