"""Formatting pass: food extras as tables, FAQ answers as short paragraphs and lists."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
L = json.load(open("data/links.json", encoding="utf-8"))
a = lambda k, t: f'<a href="{L[k]}">{t}</a>'
g = open("src/guide.html", encoding="utf-8").read()

def swap(s, start, end, new):
    i = s.index(start); j = s.index(end, i) + len(end); return s[:i] + new + s[j:]

# Food: the run-on "also good" paragraph becomes two tables in the same style as the main one
row = lambda kind, place, note, cls="": f'        <tr{cls}><td>{kind}</td><td>{place}</td><td>{note}</td></tr>\n'
ALSO = ('<p class="tablename">More we liked</p>\n      <table class="rows">\n'
 + row("Pub chain", "Wetherspoons", "The Counting House, George Square. At this point it's a UK cultural experience: mid food, decent prices, different deals every day.")
 + row("Chicken", "Nando's", "Same menu as Singapore, but better here by far.")
 + row("Indian", a("dishoom", "Dishoom"), "Nelson Mandela Place.")
 + row("Brunch", a("singlend", "The Singl-end"), "Renfrew St. Glasgow has loads of good brunch spots in the centre and West End.")
 + row("Lebanese", a("leftbank", "The Left Bank"), "Gibson St. Not that common in Singapore, so worth trying.")
 + row("Pancakes", "Stack &amp; Still", "Sweet and savoury.")
 + row("Chinese", "The West End", "Whenever you crave Chinese food and don't want to cook, there are lots of options.")
 + '      </table>\n      <p class="tablename">Outside Glasgow</p>\n      <table class="rows">\n'
 + row("Edinburgh", "Makars Mash Bar", "Bank St. Very famous; worth it if you're a foodie.")
 + row("Edinburgh", "Bertie's", "Victoria St. Might be the best fish and chips in Scotland.")
 + row("St Andrews", "Cheesy Toast Shack", "East Sands. So good.")
 + row("St Andrews", "Jannettas Gelateria", "South St. Also so good.")
 + '      </table>')
g = swap(g, '<p class="food__also">', "</p>", ALSO)

# FAQ: short paragraphs, lists where an answer lists things
Q = lambda q, ans, op="": f'    <details{op}><summary>{q}</summary><div>{ans}</div></details>\n'
ul = lambda *items: "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
FAQ = ('<div class="faq__list">\n'
 + Q("What should I pack?", "<p>Scotland is wet, rocky and slippery, and the weather changes all the time. The things we were glad we brought:</p>"
     + ul("<b>Hiking shoes</b>, or any shoes with real grip.", "<b>Uniqlo Heattech (Extra Warm).</b> It saved my life multiple times.",
          "<b>Two or more shopping bags.</b> Every shop charges for plastic bags.",
          "<b>Extension cords.</b> UK plugs are the same as Singapore's, so you only need adapters for EU trips.",
          "<b>Downloaded shows.</b> Data is patchy in the Highlands and on long journeys."), " open")
 + Q("Are lectures recorded?", "<p>Not in our experience. Each lecturer decides, and none of ours were.</p><p>Attendance is different for every lecturer (QR code, password or a paper sheet), so don't skip anything in week 1. For MAE and EEE it turned out to be very relaxed.</p>")
 + Q("When do exam timetables come out?", f"<p>Annoyingly late: about five weeks before exams, on Pegasus.</p>"
     + ul("Semester 1: first week of November (exams 7–18 Dec in 2026/27).", "Semester 2: early March (exams 19 Apr – 21 May 2027).")
     + f"<p>Each one is a draft for a week, then final ({a('strath_exams', 'exam timetable FAQs')}). Book flights home with a flexible fare.</p>")
 + Q("Which hall should I pick?", "<p>If you stay in Strath's halls, we'd go single-gender: the flats are a lot more spacious.</p>"
     + ul("<b>Thomas Campbell Court</b>: 4-bedroom flats sharing 1 bathroom, £146.16 a week.", "<b>Birkbeck Court</b>: 6-bedroom flats with 2 bathrooms, £146.16 a week.",
          "<b>Andrew Ure, Forbes and Garnett</b>: rooms with a wash basin, £154.56 a week. Handy for washing small things and drying them on the radiator.")
     + f"<p>Mixed flats mean more people: more fun, but a higher chance of a bad flatmate. See {a('strath_accom', 'exchange accommodation')}.</p>")
 + Q("What does a semester in halls cost?", f"<p>At 2026/27 prices:</p>"
     + ul("Semester 1 let (14 weeks 2 days): about £2,090 for a standard room, £2,210 with a basin.", "Semester 2 let (21 weeks 5 days): about £3,170, or £3,360 with a basin.")
     + f"<p>Semester 1 rooms are limited, so apply early through the {a('strath_accom', 'Accommodation Portal')}.</p>")
 + Q("Anything weird about halls?", ul("Fire drills every Wednesday &gt;:( One was at 8 in the morning.", "Laundry at Lord Todd is about S$5 a wash and dry. Detergent isn't included; the app may give you a free cycle.",
     "Kitchens have a fridge, freezer, microwave, kettle and oven, but no air fryer.", "Cleaners do the shared areas a couple of times a semester.",
     "Checking out is relaxed: clear your room, donate pots and pans in the boxes by the halls, and drop your keys at Lord Todd."))
 + Q("What if something goes wrong?", ul("<b>999</b> for emergencies.", "<b>111</b> (NHS 24) for urgent health advice that isn't an emergency.",
     f"Keep NTU's ISOS app on your phone, and {a('mfa_eregister', 'eRegister with MFA')} so Singapore can reach you."))
 + Q("What's the time difference with Singapore?", "<p>Singapore is 8 hours ahead of Glasgow from late October to late March, and 7 hours ahead the rest of the year, when the UK is on summer time.</p><p>Lunch in Glasgow is evening in Singapore, so that's the easy time to call home.</p>")
 + Q("Can I rent privately instead of halls?", f"<p>You can, but for one semester halls are much simpler, and halls are exempt from council tax.</p><p>In a private flat, ask Strath for a student status letter for the council. Whether you get the exemption is the council's decision. See {a('strath_accom', 'Strath accommodation')}.</p>")
 + Q("How does the student card work?", f"<p>Most students never need a physical card: once you register, your {a('strath_card', 'digital student card')} is in the Strathclyde app.</p><p>If you want a plastic one, ask at the Teaching and Learning Building. It was free when we went.</p>")
 + Q("Is the NHS free for me?", f"<p>Don't count on it. {a('nhs', 'NHS Scotland')}'s free care for students is tied to a student visa, and you enter as a visitor.</p><p>NTU's {a('ntu_insurance', 'Group Travel Insurance')} (Chubb) covers sanctioned exchange travel, so read what it includes before you fly.</p>")
 + Q("Which SIM card?", ul(f"<b>{a('lebara', 'Lebara')}</b> if you'll travel in Europe: 100 GB for £20 per 30 days, with EU roaming included.",
     f"<b>{a('voxi', 'VOXI')}</b> (Vodafone) has good eSIM deals, but roaming in Europe needs a pass: £2.60 a day, £15 for 8 days, £20 for 15 days.",
     "You can also buy SIM cards at the counter of almost any supermarket."))
 + Q("How much cash do I need?", f"<p>About £100 for the whole exchange. 95% of places take cards, buses included, and when you split bills with international friends they'll often pay you back in cash anyway.</p><p>Open a {a('monzo', 'Monzo')} account early: Groupon kept rejecting our Singapore cards, and some memberships only take a UK Direct Debit.</p>")
 + Q("How do buses work?", "<p>Every company does it differently, but they all take contactless cards like YouTrip or Wise. We ran into four systems:</p>"
     + ul("Tap on and tap off, like in Singapore.", "Tap on for one flat fare, however far you go.", "Tell the driver your stop and tap the fare they key in.", "Book online in advance, mostly for long routes.")
     + f"<p>Under 22 and living in Scotland? Buses are free with a {a('nec', 'National Entitlement Card')}. And everyone jaywalks, but the lights work very differently from Singapore's, so watch them for a few days first.</p>")
 + Q("Where do I buy groceries?", ul("<b>ALDI</b> (High Street) and <b>LIDL</b> (Duke Street) are closest. LIDL is a bit more of a walk but has better stuff, so get the LIDL Plus app.",
     "<b>Savers</b> for proper brands (Pantene, Dove, TRESemmé) for dirt cheap. <b>Poundland</b> for the cheapest of the cheap.",
     f"<b>{a('chungying', 'Chung Ying')}</b> (254 Dobbie's Loan): an Asian supermarket. Kinda overpriced, but a dream.",
     "<b>Primark</b> for cheap clothes and shoes, <b>Mountain Warehouse</b> for hiking gear."))
 + Q("Which meal deal?", "<p>A meal deal is a main, a snack and a drink for about £4.</p>"
     + ul(f"<b>{a('tesco_md', 'Tesco')}</b>: £3.85 with Clubcard, and the best quality.", "<b>Boots</b> (Buchanan Galleries): the cheapest we found, plus a clearance shelf.",
          "<b>Co-op</b>: take the Ginsters Cornish pasty as your snack. It's as filling as a main.", f"<b>Greggs</b>: a free sausage roll with a cold Sandwich Deal if you show {a('greggs_sb', 'Student Beans')}.",
          "<b>M&amp;S</b>: the fancy one."))
 + Q("Is National Trust for Scotland worth it?", f"<p>{a('nts_join', 'Membership')} is £6.60 a month, or £3.80 on the Young rate, and gets you into every NTS castle, house and garden. Entry is usually £15–20, so it pays off fast.</p><p>The catch: you can't cancel during the first year, so it's really £79.20 (£45.60 Young). Under 22 with a National Entitlement Card? {a('hes_faq', 'Historic Environment Scotland')} castles cost just £1.</p>")
 + Q("What British food is worth ordering?", "<p>Gonna be honest, you don't come to the UK for the food. But these are worth it:</p>"
     + ul("Cullen skink (smoked haddock soup).", "Steak and ale pie, and shepherd's or cottage pie.", "Haggis, neeps and tatties. I love haggis.", "Sticky toffee pudding: the best thing Britain ever invented.",
          "A deep-fried Mars bar. Everyone hates me for saying this, but it's actually so good.", "Sunday roast, but only at a carvery or a good steakhouse.")
     + "<p>Chippies are a bit of a scam once you add sauces and sides (a meal can pass £20), but go once for the vibe. \"Supper\" means it comes with chips.</p>")
 + Q("Best hikes?", ul("<b>Old Man of Storr</b> (Skye): the most scenic, if the wind lets you up.", "<b>Goatfell</b> (Arran): take the first ferry over and the last one back.",
     "<b>Arthur's Seat</b> (Edinburgh): easy and scenic, but the last bit to the very top is bare rock and a bit sketchy.", "<b>Ben Nevis</b>: we didn't make it, but heard great things."))
 + Q("Where can I see the northern lights?", f"<p>Not really in Glasgow: there's too much light pollution. I tried at the Necropolis on a high-activity night and it was 90% cloudy. Calton Hill in Edinburgh sometimes works.</p><p>Shetland is the best bet in Scotland: {a('northlink', 'NorthLink')}'s overnight ferry from Aberdeen, from £29.50 one way (2027 low season). Go early in the semester, while the nights are long. Iceland, Norway and Finland work too, but they're expensive.</p>")
 + Q("What do people do in the evenings?", ul(f"{a('stand', 'The Stand')}'s Sunday improv: £1 for students.", "Concerts, festivals and musicals, often cheaper than in Singapore.",
     "Kitty O'Shea's for live music, and Maggie's for line dancing and rodeo nights.", "On campus: Drag Bingo, Therapets, boxing and spin classes, and Strath Active events like UV badminton.",
     "Slow days: Waterstones and the West End's secondhand bookshops."))
 + '  </div>')
g = swap(g, '<div class="faq__list">', "  </div>", FAQ)
open("src/guide.html", "w", encoding="utf-8").write(g)

css = open("css/site.css", encoding="utf-8").read()
add = """
/* Text rhythm inside answers and intros */
.faq details > div { display: grid; gap: 0.75em; }
.faq details > div ul { margin: 0; padding-left: 1.15em; display: grid; gap: 0.45em; }
.faq details > div li::marker { color: var(--muted); }
.faq details > div b { font-weight: 500; }
.intro__cols p, .food__lead, .dates__note, .around__note { line-height: 1.6; }
.food__tables .tablename { margin-top: 40px; }
.food__tables .tablename:first-child { margin-top: 0; }
"""
open("css/site.css", "w", encoding="utf-8").write(css + add)
print("format pass applied")
