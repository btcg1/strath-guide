"""Copy pass in the author's own voice (from the original Strath Guide doc): more context where it helps, still fact-checked."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
L = json.load(open("data/links.json", encoding="utf-8"))
a = lambda k, t: f'<a href="{L[k]}">{t}</a>'

def sub_block(s, start, end, new):
    i = s.index(start); j = s.index(end, i) + len(end)
    return s[:i] + new + s[j:]
def rep(s, pairs):
    for x, y in pairs:
        assert s.count(x) == 1, (s.count(x), x[:90]); s = s.replace(x, y)
    return s

# ---------- build.py: the four panels ----------
b = open("tools/build.py", encoding="utf-8").read()
VERBS = '''VERBS = [
 ("apply", "Apply", f"<p>You apply through NTU's {A('gem_explorer', 'GEM Explorer')} on the {A('gem_portal', 'GEM Mobility Portal')}. You need two NTU semesters done, a CGPA of 3.3 or more, and no earlier in-person exchange. You rank three universities, and NTU allocates places by CGPA band, citizenship, your ranking and how many spots each school has.</p><ul><li>{A('strath_partners', 'Strathclyde takes nominations')} 1 March – 15 May for a September start and 15 September – 15 October for January. NTU does the nominating; you just wait for Strath's email.</li><li>Then you apply to Strath online with your passport, NTU transcript and class choices.</li></ul>"),
 ("match", "Match", f"<p>Course matching is the part everyone panics about. Find past matches in {A('coursefinder', 'CourseFinder')}, then submit each one in NTU's {A('coursematching', 'online course matching system')} (both need your NTU login).</p><ul><li>Pick from Strath's {A('strath_classes', 'exchange class catalogue')} and check for timetable clashes yourself.</li><li>Officially Strath allows classes from at most two departments. Honestly, don't stress: NTU is known at Strath for being a headache to course-match, so the coordinators are flexible as long as most of your classes are in your primary department. One of us (MAE) had MAE, EEE and DMEM classes approved.</li><li>Exchange grades count towards your AUs, not your CGPA.</li></ul>"),
 ("fly", "Fly", f"<p>Get a {A('eta', 'UK ETA')} before you fly: £20 on GOV.UK or the UK ETA app. It's usually decided within a day, but give it 3 working days. It lasts 2 years.</p><ul><li>You enter as a {A('visit_study', 'Standard Visitor')}, which lets you study for up to 6 months but not work, not even an unpaid internship.</li><li>Carry your acceptance letter, accommodation details and proof of funds, and keep your boarding pass.</li><li>Before you leave, do NTU's briefing, indemnity letter, ISOS app and {A('ntu_predep', 'Travel Registry')} declaration, and {A('mfa_eregister', 'eRegister with MFA')} for the trip.</li></ul>"),
 ("settle", "Settle", f"<p>From the airport, take the {A('airport500', 'Airport Express 500')}. It runs every 10 minutes, 24 hours a day, to Buchanan Bus Station, about a 15-minute walk from the halls. Collect your keys at Lord Todd. Right after, there's a free market of stuff past students left behind (cutlery, plates, decor, storage), so take what you need.</p><ul><li>Week one: a {A('lebara', 'UK SIM')}, a {A('railcard1625', 'Railcard')}, {A('monzo', 'Monzo')}, and the {A('esncard', 'ESNcard')} at the society fair. Get it early: it sold out last time and wasn't restocked until the end of the semester.</li><li>Then TJ Hughes in the St Enoch Centre for bedding, pans and a laundry basket. Split an Uber back four ways and it's cheap.</li><li>Go to every class in week 1. Every lecturer takes attendance differently: QR code, password or paper.</li></ul>"),
]'''
b = re.sub(r"VERBS = \[\n.*?\n\]", lambda m: VERBS, b, count=1, flags=re.S)

# places: a personal line under some names
NOTES = {
 "Isle of Skye": "Easily the most scenic hike we did (Old Man of Storr), but you need luck with the weather or you'll get blown off the mountain.",
 "Glencoe": "A must, even though it's annoying to get to.",
 "Glenfinnan": "The Harry Potter viaduct. One of the ESN tours we'd recommend.",
 "Dunkeld & Birnam": "One of my favourite places in Scotland. On a good weather day it's so scenic, very reconnect-with-nature vibes.",
 "Aviemore & Rothiemurchus": "Highly recommend. Outdoor heaven: trails, quad bikes, ziplining, horse riding.",
 "Stirling": "Very hilly, so give yourself time. If you pay for the castle, follow the free guided tour.",
 "Falkirk": "A very therapeutic walk along the canal from the Wheel to the Kelpies.",
 "New Lanark": "A surreal place. It's a steep walk down from the station.",
 "East Linton & Preston Mill": "Proper village vibes, farmers' markets and a very modern bakery.",
 "Thurso & Wick": "Only for the very adventurous: remote and peaceful, with a lovely coastal walk.",
 "Isle of Arran": "Absolutely beautiful, and close to school. I cannot recommend this island enough.",
 "Inchcolm Island": "An abandoned abbey on an uninhabited island. Queensferry, where the boat leaves, is a beautiful seaside town.",
 "Puffins & North Berwick": "Book fast when tickets drop: the cheap Puffin Express sold out in a day. We saw so many puffins, and seals too.",
 "St Andrews": "Go on a Sunday, when the Old Course opens to the public. Cheesy Toast Shack and Jannettas Gelateria are so good.",
 "Culross": "A small town that looks like the Italian countryside.",
 "Edinburgh": "Calton Hill and its café are a nice chill spot. Bertie's might be the best fish and chips in Scotland.",
 "Cathedral & Necropolis": "Walkable from school, and great at golden hour.",
 "Pollok Park & the Burrell": "Highland cows up close, and a free art museum.",
}
b = b.replace("PLACE_LINK = ", f"PLACE_NOTE = {NOTES!r}\nPLACE_LINK = ", 1)
b = rep(b, [('''        lis.append(f'<li class="index__row"{ti}{prev}>{thumb}{nm}<span class="index__info">{info}</span></li>')''',
             '''        nt = f'<span class="index__note">{esc(PLACE_NOTE[name])}</span>' if name in PLACE_NOTE else ''
        lis.append(f'<li class="index__row"{ti}{prev}>{thumb}{nm}<span class="index__info">{info}</span>{nt}</li>')''')])
open("tools/build.py", "w", encoding="utf-8").write(b)

# ---------- trips.json: personal lines ----------
t = json.load(open("data/trips.json", encoding="utf-8"))
LINES = {
 "oban": "ESN day tour, and one we'd recommend: the seaside town under McCaig's Tower, plus Inveraray and Kilchurn Castle on the way.",
 "glenfinnan": "ESN day tour to the Harry Potter viaduct, via Luss on Loch Lomond and Fort William.",
 "falkirk": "A very therapeutic canal walk from the Falkirk Wheel to the Kelpies.",
 "inchcolm": "An abandoned abbey on an uninhabited island. The boat leaves from Queensferry, a beautiful seaside town under the Forth Bridge.",
 "lochness": "A long ESN day: Glencoe, the Commando Memorial, Fort Augustus and Urquhart Castle.",
 "stirling": "Castle and Wallace Monument, both up very steep hills. Give yourself more time than you think.",
 "skye": "Our best weekend. Eilean Donan, Portree, Sligachan and the Old Man of Storr, the most scenic hike we did.",
 "culross": "A small town that looks like the Italian countryside.",
 "standrews": "Go on a Sunday, when the Old Course opens to the public. Cheesy Toast Shack and Jannettas are so good.",
 "arran": "Absolutely beautiful and close to school. First ferry over, last ferry back. I cannot recommend this island enough.",
 "newlanark": "A surreal mill village by the Falls of Clyde. Very hilly from the station.",
 "dunkeld": "One of my favourite places in Scotland: the Hermitage, a 600-year-old oak and the river.",
 "inverness": "Culloden, Fort George, Rothiemurchus (outdoor heaven) and the far north coast at Wick.",
}
for x in t:
    if x["id"] in LINES: x["line"] = LINES[x["id"]]
json.dump(t, open("data/trips.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- guide page ----------
g = open("src/guide.html", encoding="utf-8").read()
g = rep(g, [
 ("Getting from NTU to Strathclyde for a semester: applying, course matching, the ETA, costs, halls and daily life in Glasgow.",
  "Everything we wish someone had told us before our semester at Strathclyde: applying, course matching, the ETA, money, halls and daily life in Glasgow."),
 ("Singapore dollars to the pound, <span data-fx-when>on 24 Oct 2026</span>.</span>",
  "Singapore dollars to the pound, <span data-fx-when>on 24 Oct 2026</span>. Menu prices look like Singapore's, but they're in pounds.</span>"),
 (": unlimited buses for a day.</span>", ": unlimited buses for a day. Perfect for St Andrews and the Fife coast.</span>"),
 (" with Clubcard (£4.25 without).</span>", " with Clubcard (£4.25 without): main, snack and drink. A lifesaver when you're too lazy to cook.</span>"),
])
FOOD = f'''<p class="tablename">Glasgow</p>
      <table class="rows">
        <tr><td>Breakfast</td><td>Joanna Goodbite</td><td>George St. Full Scottish breakfast; the whole stretch near campus has cheap deals.</td></tr>
        <tr><td>Chinese</td><td>Friends Chinese Café</td><td>273 High St. Cash only, authentic, 10% off the main menu if you say you're a student.</td></tr>
        <tr><td>Curry</td><td>{a('curryhouse', 'Curry House')}</td><td>80 West Nile St. Proper, filling food for £5–6. Banger food.</td></tr>
        <tr><td>Shawarma</td><td>Rosto Shawarma</td><td>186 London Rd, by the Barras. Top tier and reasonably priced.</td></tr>
        <tr class="gap"><td>Cheap fine dining</td><td>{a('scholars', 'Scholars')}</td><td>Cathedral St. Cooked and served by culinary students, like the restaurant at Temasek Poly.</td></tr>
        <tr><td>Raclette</td><td>{a('cheesebox', 'Cheese Box')}</td><td>Merchant City. Swiss food from a converted police box. Cute place, decent food.</td></tr>
        <tr><td>Falafel</td><td>Falafel To Go</td><td>Hope St. About £5. Cheap, vegetarian friendly, good quality.</td></tr>
        <tr><td>Pizza</td><td>{a('revolution', 'Revolution')}</td><td>Mitchell St. Pizzas for about £7.</td></tr>
        <tr class="gap"><td>Pizza</td><td>{a('paesano', 'Paesano')}</td><td>94 Miller St. Might be the best pizza in Glasgow.</td></tr>
        <tr><td>Scottish</td><td>{a('gandolfi', 'Café Gandolfi')}</td><td>64 Albion St. Local food with really good ingredients.</td></tr>
        <tr><td>Chinese</td><td>{a('holeefook', 'Ho Lee Fook')}</td><td>1 MacFarlane St. Just go cus of the name.</td></tr>
        <tr><td>Burgers</td><td>{a('bmb', 'Bread Meats Bread')}</td><td>65 St Vincent St. Great if you wanna get fat.</td></tr>
        <tr class="gap"><td>Buffet</td><td>{a('cosmo', 'COSMO')}</td><td>St Enoch Centre. Weekday lunch is worth it; quality is mid, but the variety is huge.</td></tr>
        <tr><td>Sunday roast</td><td>{a('merchant', 'The Merchant Steakhouse')}</td><td>56 Ingram St. Our one expensive rec: a very good Sunday roast, close to school.</td></tr>
      </table>
      <p class="food__also">Wetherspoons (The Counting House, George Square) is a UK cultural experience at this point: mid food, decent prices, different deals every day. Nando's here is better than Singapore's by far. Also good: {a('dishoom', 'Dishoom')} (Nelson Mandela Place), {a('singlend', 'The Singl-end')} (Renfrew St), {a('leftbank', 'The Left Bank')} (Gibson St, try the Lebanese food), Kozi (49 High St) and Stack &amp; Still for pancakes. Craving Chinese food and too lazy to cook? Head to the West End. In Edinburgh, Makars Mash Bar and Bertie's; in St Andrews, Cheesy Toast Shack and Jannettas.</p>'''
g = sub_block(g, '<p class="tablename">Glasgow</p>', "</p>\n    </div>\n  </div>\n</section>", FOOD + "\n    </div>\n  </div>\n</section>")
g = rep(g, [('<h2 class="h2 food__title">Where we ate, and what it&nbsp;cost</h2>',
             '<h2 class="h2 food__title">Where we ate, and what it&nbsp;cost</h2>\n  <p class="food__lead">Honestly, you don\'t come to the UK for the food. The Middle Eastern and Indian food, on the other hand, is top tier. Everything here we tried ourselves, so it\'s subjective.</p>')])

Q = lambda q, ans, op="": f'    <details{op}><summary>{q}</summary><div>{ans}</div></details>\n'
FAQ = ('<div class="faq__list">\n'
 + Q("What should I pack?", "<p>Hiking shoes or anything with real grip: Scotland is wet, rocky and slippery. Uniqlo Heattech (Extra Warm) saved my life multiple times. Bring at least two shopping bags, because every shop charges for plastic bags, and an extension cord or two. UK plugs are the same as Singapore's, so you only need adapters for EU trips. Download some shows too: data is patchy in the Highlands and on long journeys.</p>", " open")
 + Q("Are lectures recorded?", "<p>Not in our experience: each lecturer decides, and none of ours were. Attendance is different for every lecturer (QR code, password or paper), so don't skip anything in week 1. For MAE and EEE, attendance turned out to be very relaxed.</p>")
 + Q("When do exam timetables come out?", f"<p>Annoyingly late: about five weeks before exams, on Pegasus. That's the first week of November for semester 1 and early March for semester 2. Each one is a draft for a week, then final. In 2026/27 the assessment periods are 7–18 December and 19 April – 21 May ({a('strath_exams', 'exam timetable FAQs')}). Book flights home with a flexible fare.</p>")
 + Q("Which hall should I pick?", f"<p>If you stay in Strath's halls, we'd go single-gender: the flats are a lot more spacious. Thomas Campbell Court has 4-bedroom flats sharing 1 bathroom (£146.16 a week). Birkbeck Court has 6-bedroom flats with 2 bathrooms (£146.16). Andrew Ure, Forbes and Garnett have rooms with a wash basin (£154.56), handy for washing small things and drying them on the radiator. Mixed flats mean more people: more fun, but a higher chance of a bad flatmate. {a('strath_accom', 'Exchange accommodation')}.</p>")
 + Q("What does a semester in halls cost?", f"<p>A semester 1 let (14 weeks 2 days) is about £2,090 for a standard room or £2,210 with a basin. A semester 2 let (21 weeks 5 days) is about £3,170 or £3,360. Semester 1 rooms are limited, so apply early through the {a('strath_accom', 'Accommodation Portal')}.</p>")
 + Q("Anything weird about halls?", "<p>Fire drills every Wednesday &gt;:( One was at 8 in the morning. Laundry at Lord Todd is about S$5 a wash and dry, and detergent isn't included (the app may give you a free cycle). Kitchens have a fridge, freezer, microwave, kettle and oven, but no air fryer. Cleaners do the shared areas a couple of times a semester. Checking out is relaxed: clear your room, donate pots and pans in the boxes by the halls, and drop your keys at Lord Todd.</p>")
 + Q("Is the NHS free for me?", f"<p>Don't count on it. {a('nhs', 'NHS Scotland')}'s free care for students is tied to a student visa, and you enter as a visitor. NTU's {a('ntu_insurance', 'Group Travel Insurance')} (Chubb) covers sanctioned exchange travel, so read what it includes.</p>")
 + Q("Which SIM card?", f"<p>{a('lebara', 'Lebara')} if you'll travel in Europe: 100 GB for £20 per 30 days, with EU roaming included. {a('voxi', 'VOXI')} (Vodafone) has good eSIM deals, but roaming in Europe needs a pass (£2.60 a day, £15 for 8 days, £20 for 15 days). You can also buy SIM cards at most supermarket counters.</p>")
 + Q("How much cash do I need?", f"<p>About £100 for the whole exchange. 95% of places take cards, buses included, and when you split bills with international friends they'll often pay you back in cash anyway. Open a {a('monzo', 'Monzo')} account early: Groupon kept rejecting our Singapore cards, and some memberships only take a UK Direct Debit.</p>")
 + Q("How do buses work?", f"<p>Every company does it differently, but they all take contactless cards like YouTrip or Wise. We ran into four systems: tap on and tap off like in Singapore; tap on for one flat fare however far you go; tell the driver your stop and tap what they key in; and book online ahead, mostly for long routes. Under 22 and living in Scotland? Buses are free with a {a('nec', 'National Entitlement Card')}.</p><p>Everyone jaywalks, but the traffic lights work very differently from Singapore's, so watch them for a few days first.</p>")
 + Q("Where do I buy groceries?", f"<p>ALDI (High Street) and LIDL (Duke Street) are the closest. Both are cheap with lots of own-brand stuff; LIDL is a bit more of a walk but has better stuff, so get the LIDL Plus app. Savers sells proper brands (Pantene, Dove, TRESemmé) for dirt cheap, and Poundland is the cheapest of the cheap. {a('chungying', 'Chung Ying')} (254 Dobbie's Loan) is an Asian supermarket: kinda overpriced, but a dream. Primark for cheap clothes, Mountain Warehouse for hiking gear.</p>")
 + Q("Which meal deal?", f"<p>{a('tesco_md', 'Tesco')} is £3.85 with Clubcard and has the best quality. Boots at Buchanan Galleries was the cheapest we found, with a clearance shelf. At Co-op take the Ginsters Cornish pasty as your snack: it's as filling as a main. Greggs throws in a free sausage roll with a cold Sandwich Deal if you show {a('greggs_sb', 'Student Beans')}. M&amp;S is the fancy one.</p>")
 + Q("Is National Trust for Scotland worth it?", f"<p>{a('nts_join', 'Membership')} is £6.60 a month, or £3.80 on the Young rate, and gets you into every NTS castle, house and garden. Entry is usually £15–20, so it pays off fast, but you can't cancel during the first year, so it's really £79.20 (£45.60 Young). Under 22 with a National Entitlement Card? {a('hes_faq', 'Historic Environment Scotland')} castles cost just £1.</p>")
 + Q("What British food is worth ordering?", "<p>Gonna be honest, you don't come to the UK for the food. But: cullen skink (smoked haddock soup), steak and ale pie, shepherd's or cottage pie, haggis neeps and tatties (I love haggis), and sticky toffee pudding, the best thing Britain ever invented. Deep-fried Mars bar too; everyone hates me for saying this, but it's actually so good. Have Sunday roast only at a carvery or a good steakhouse. Chippies are a bit of a scam once you add sauces and sides (a meal can pass £20), but go once for the vibe. \"Supper\" means it comes with chips.</p>")
 + Q("Best hikes?", "<p>Old Man of Storr on Skye was the most scenic, if the wind lets you up. Goatfell on Arran if you take the first ferry over and the last one back. Arthur's Seat in Edinburgh is easy and scenic, but the last bit to the very top is bare rock and a bit sketchy. We didn't make it up Ben Nevis.</p>")
 + Q("Where can I see the northern lights?", f"<p>Not really in Glasgow: too much light pollution. I tried at the Necropolis on a high-activity night and it was 90% cloudy. Calton Hill in Edinburgh sometimes works. Shetland is the best bet in Scotland: {a('northlink', 'NorthLink')}'s overnight ferry from Aberdeen, from £29.50 one way (2027 low season). Go early in the semester, while the nights are long. Iceland, Norway and Finland work too, but they're expensive.</p>")
 + Q("What do people do in the evenings?", f"<p>{a('stand', 'The Stand')}'s Sunday improv is £1 for students. Concerts, festivals and musicals here are often cheaper than in Singapore. Kitty O'Shea's is a cool Irish pub with live music, and Maggie's does line dancing and rodeo nights. On campus there's Drag Bingo, Therapets, boxing and spin classes, and Strath Active events like UV badminton. Waterstones and the West End's secondhand bookshops for slow days.</p>")
 + '  </div>')
g = sub_block(g, '<div class="faq__list">', "</div>\n</section>", FAQ + "\n</section>")
open("src/guide.html", "w", encoding="utf-8").write(g)

# ---------- travel page ----------
tr = open("src/travel.html", encoding="utf-8").read()
tr = rep(tr, [("Where we went from Glasgow in one semester: 24 trips on a map, 36 places with prices and opening times, and our photos.</p>\n    <div",
               "Every weekend we could, we left Glasgow. Here's where we went: 24 trips on a map, 36 places with prices and opening times, and way too many photos.</p>\n    <div"),
              ("Every pin is a trip we took in semester 1, 2025,", "Strath is in an amazing spot for travelling: four stations are a walk from the halls. Every pin is a trip we took in semester 1, 2025,")])
open("src/travel.html", "w", encoding="utf-8").write(tr)

css = open("css/site.css", encoding="utf-8").read()
css = rep(css, [(".index__note {", ".index__note {")] if ".index__note {" in css else [
 (".index__thumb { display: none; }", ".index__thumb { display: none; }\n.index__note { grid-column: 2; font-size: var(--step-small); color: var(--ink); max-width: 60ch; margin-top: 2px; }\n.food__lead { margin-top: 20px; max-width: 58ch; }")])
css = rep(css, [("  .index__row[data-nothumb] { grid-template-columns: minmax(0, 1fr); padding-left: 98px; }",
                 "  .index__row[data-nothumb] { grid-template-columns: minmax(0, 1fr); padding-left: 98px; }\n  .index__note { grid-column: 2; }\n  .index__row[data-nothumb] .index__note { grid-column: 1; }")])
open("css/site.css", "w", encoding="utf-8").write(css)
print("voice pass applied")
