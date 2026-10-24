"""One-time restructure: split src/template.html into src/guide.html (essentials) and src/travel.html (trips), with tabs and links."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
T = open("src/template.html", encoding="utf-8").read()
L = json.load(open("data/links.json", encoding="utf-8"))
a = lambda key, text: f'<a href="{L[key]}">{text}</a>'

def cut(start, end, s=T, frm=0):
    i = s.index(start, frm); j = s.index(end, i) + len(end); return s[i:j]

head = T[:T.index("<body>\n") + len("<body>\n")]
sec = {k: cut(m, "</section>") for k, m in {
    "intro": '<section class="intro"', "trips": '<section class="trips" id="trips">', "verbs": '<section class="verbs" id="apply"',
    "costs": '<section class="costs" id="costs">', "around": '<section class="around" id="around">', "year": '<section class="year" id="year">',
    "places": '<section class="places" id="places">', "photos": '<section class="roll" id="photos">', "food": '<section class="food" id="food">',
    "faq": '<section class="faq" id="faq">', "sources": '<section class="sources" id="sources">'}.items()}
dialog = cut('<dialog class="lightbox"', "</dialog>")
scripts = T[T.index("<script>window.TRIPS"):]

def rep(s, pairs):
    for x, y in pairs:
        assert s.count(x) == 1, (s.count(x), x[:80]); s = s.replace(x, y)
    return s

# Links inside sections
sec["costs"] = rep(sec["costs"], [
 ("Pounds a week for a standard room in halls, 2026/27 semester let.", f"Pounds a week for a standard room in {a('strath_accom', 'halls')}, 2026/27 semester let."),
 ("Pounds a year for a Railcard: a third off most train fares.", f"Pounds a year for a {a('railcard1625', 'Railcard')}: a third off most train fares."),
 ("Pounds for the UK ETA you need before you fly.", f"Pounds for the {a('eta', 'UK ETA')} you need before you fly."),
 ("Pounds for a Stagecoach East Scotland DayRider: unlimited buses for a day.", f"Pounds for a {a('dayrider', 'Stagecoach East Scotland DayRider')}: unlimited buses for a day."),
 ("Pounds for a Tesco meal deal with Clubcard (£4.25 without).", f"Pounds for a {a('tesco_md', 'Tesco meal deal')} with Clubcard (£4.25 without)."),
])
sec["around"] = rep(sec["around"], [
 ("<td>15 min walk. Airport 500 at stance 46</td>", f"<td>15 min walk. {a('airport500', 'Airport 500')} at stance 46</td>"),
 ("<td>16–25 Railcard</td>", f"<td>{a('railcard1625', '16–25 Railcard')}</td>"),
 ("<td>26–30 Railcard</td>", f"<td>{a('railcard2630', '26–30 Railcard')}</td>"),
 ("<td>National Entitlement Card</td>", f"<td>{a('nec', 'National Entitlement Card')}</td>"),
 ("<td>Stagecoach DayRider</td>", f"<td>{a('dayrider', 'Stagecoach DayRider')}</td>"),
 ("<td>Flixbus</td><td>20% off with Student Beans</td>", f"<td>{a('flixbus', 'Flixbus')}</td><td>{a('flix_sb', '20% off with Student Beans')}</td>"),
 ("<td>Ember to Fort William</td>", f"<td>{a('ember', 'Ember')} to Fort William</td>"),
 ("<td>Citylink/Ulsterbus 923 to Belfast</td>", f"<td>{a('belfast923', 'Citylink/Ulsterbus 923')} to Belfast</td>"),
 ("<p class=\"around__note\">ScotRail dropped", f"<p class=\"around__note\">{a('scotrail', 'ScotRail')} dropped"),
 ("ScotRail</a> dropped peak fares for good", "ScotRail</a> dropped peak fares for good"),
])
food_links = [("Curry House", "curryhouse"), ("Scholars", "scholars"), ("Cheese Box", "cheesebox"), ("Revolution", "revolution"), ("Paesano", "paesano"),
              ("Café Gandolfi", "gandolfi"), ("Ho Lee Fook", "holeefook"), ("Bread Meats Bread", "bmb"), ("COSMO", "cosmo"), ("The Merchant Steakhouse", "merchant")]
sec["food"] = rep(sec["food"], [(f"<td>{n}</td>", f"<td>{a(k, n)}</td>") for n, k in food_links] + [
 ("Also good: Dishoom (Nelson Mandela Place), The Singl-end (Renfrew St), The Left Bank (Gibson St),",
  f"Also good: {a('dishoom', 'Dishoom')} (Nelson Mandela Place), {a('singlend', 'The Singl-end')} (Renfrew St), {a('leftbank', 'The Left Bank')} (Gibson St),"),
])
sec["faq"] = rep(sec["faq"], [
 ("Each lecturer decides, and none of ours were.", "Each lecturer decides, and none of ours were."),
 ("About five weeks before exams, on Pegasus:", f"About five weeks before exams, on Pegasus ({a('strath_exams', 'Strathclyde exam FAQs')}):"),
 ("Single-gender flats felt roomier.</p>", f"Single-gender flats felt roomier. {a('strath_accom', 'Exchange accommodation')}.</p>"),
 ("so apply early through the Accommodation Portal.", f"so apply early through the {a('strath_accom', 'Accommodation Portal')}."),
 ("NHS Scotland's free care for students is tied to a student visa,", f"{a('nhs', 'NHS Scotland')}'s free care for students is tied to a student visa,"),
 ("NTU's Group Travel Insurance (Chubb) covers", f"NTU's {a('ntu_insurance', 'Group Travel Insurance')} (Chubb) covers"),
 ("<p>Lebara: 100 GB", f"<p>{a('lebara', 'Lebara')}: 100 GB"),
 ("VOXI: eSIM, but Europe", f"{a('voxi', 'VOXI')}: eSIM, but Europe"),
 ("Open a Monzo account", f"Open a {a('monzo', 'Monzo')} account"),
 ("Chung Ying (254 Dobbie's Loan)", f"{a('chungying', 'Chung Ying')} (254 Dobbie's Loan)"),
 ("<p>Tesco is £3.85 with Clubcard.", f"<p>{a('tesco_md', 'Tesco')} is £3.85 with Clubcard."),
 ("Greggs gives a free sausage roll with a cold Sandwich Deal if you show Student Beans.", f"Greggs gives a free sausage roll with a cold Sandwich Deal if you show {a('greggs_sb', 'Student Beans')}."),
 ("<p>£6.60 a month, or £3.80 on the Young rate,", f"<p>{a('nts_join', 'NTS membership')} is £6.60 a month, or £3.80 on the Young rate,"),
 ("Historic Environment Scotland castles cost £1.", f"{a('hes_faq', 'Historic Environment Scotland')} castles cost £1."),
 ("NorthLink's overnight ferry from Aberdeen,", f"{a('northlink', 'NorthLink')}'s overnight ferry from Aberdeen,"),
 ("<p>The Stand's Sunday improv", f"<p>{a('stand', 'The Stand')}'s Sunday improv"),
])
sec["year"] = rep(sec["year"], [
 ("Here are Strathclyde's 2026/27 dates against them.", f"Here are {a('strath_keydates', 'Strathclyde’s 2026/27 dates')} against them."),
])

def nav(page):
    tabs = (f'<a href="index.html"{" aria-current=\"page\"" if page == "guide" else ""}>Guide</a>'
            f'<a href="travel.html"{" aria-current=\"page\"" if page == "travel" else ""}>Travel</a>')
    links = ('<a href="#apply">Apply</a><a href="#costs">Costs</a><a href="#faq">FAQ</a>' if page == "guide"
             else '<a href="#trips">Map</a><a href="#places">Places</a><a href="#photos">Photos</a>')
    return (f'  <nav class="topnav" aria-label="Main">\n    <a class="wordmark" href="index.html">Strath Field Guide</a>\n'
            f'    <div class="tabs" aria-label="Pages">{tabs}</div>\n    <div class="topnav__links">{links}</div>\n  </nav>\n')

def hero(page, w1, w2, lead, href, btn, alt_href, alt, P):
    return (f'<header class="hero" id="top">\n{nav(page)}  <div class="hero__body">\n    <h1 class="hero__title">\n'
            f'      <span class="hero__line"><span class="hero__word">{w1}</span>\n'
            f'        <span class="stripwrap"><span class="strip shutter" data-strip>\n          {{{{{P}STRIP_IMGS}}}}\n'
            f'        </span><span class="strip__caption" data-strip-caption>{{{{{P}STRIP_CAPTION0}}}}</span></span></span>\n'
            f'      <span class="hero__line hero__line--2"><span class="hero__word">{w2}</span></span>\n    </h1>\n'
            f'    <p class="hero__lead">{lead}</p>\n'
            f'    <div class="hero__actions"><a class="button" href="{href}">{btn}</a><a class="hero__alt" href="{alt_href}">{alt}</a></div>\n'
            f'    <p class="strip__caption strip__caption--phone" data-strip-caption>{{{{{P}STRIP_CAPTION0}}}}</p>\n  </div>\n</header>\n')

def footer(invite, href, btn):
    return (f'<footer class="foot">\n  <div class="foot__top">\n    <div>\n      <p class="foot__invite">{invite}</p>\n'
            f'      <a class="button button--light" href="{href}">{btn}</a>\n    </div>\n    <ul class="foot__links">\n'
            f'      <li>{a("gem_explorer", "NTU GEM Explorer")}</li>\n      <li>{a("strath_exchange", "Strathclyde exchange")}</li>\n'
            f'      <li>{a("eta", "UK ETA")}</li>\n      <li><a href="index.html#sources">All sources</a></li>\n    </ul>\n  </div>\n'
            f'  <p class="foot__legal"><span>Written by NTU students after a semester at Strathclyde. Photos are our own.</span><span>Map outline: Natural Earth.</span></p>\n'
            f'  <p class="foot__mark" aria-hidden="true">Strathclyde</p>\n</footer>\n\n')

def page(title, desc, preload, hero_html, sections, foot):
    h = head.replace("<title>Strath Field Guide</title>", f"<title>{title}</title>")
    h = h.replace('<meta name="description" content="', f'<meta name="description" content="{desc}" data-old="', 1)
    h = h.replace('<link rel="preload" as="image" href="{{STRIP0}}" fetchpriority="high">', f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">')
    import re
    h = re.sub(r' data-old="[^"]*"', "", h)
    return h + hero_html + "\n<main>\n" + "\n\n".join(sections) + "\n</main>\n\n" + foot + dialog + "\n\n" + scripts

guide = page("Strath Field Guide",
    "How to get from NTU to the University of Strathclyde for a semester: applying, course matching, the UK ETA, costs, halls, food and FAQs.",
    "{{G_STRIP0}}",
    hero("guide", "NTU to", "Strathclyde", "Getting from NTU to Strathclyde for a semester: applying, course matching, the ETA, costs, halls and daily life in Glasgow.",
         "#apply", "How to apply", "travel.html", "Trips and places", "G_"),
    [sec[k] for k in ("verbs", "costs", "around", "food", "faq", "sources")],
    footer("Then go and see&nbsp;Scotland", "travel.html", "Trips and places"))
travel = page("Travel – Strath Field Guide",
    "Where we went from Glasgow in one semester: 24 trips on a map, 36 places with prices and opening times, and our photos.",
    "{{STRIP0}}",
    hero("travel", "Glasgow to", "and back", "Where we went from Glasgow in one semester: 24 trips on a map, 36 places with prices and opening times, and our photos.",
         "#trips", "See the trips", "index.html#apply", "How to apply", ""),
    [sec[k] for k in ("intro", "trips", "year", "places", "photos")],
    footer("See you in&nbsp;Glasgow", "index.html#apply", "How to apply"))
open("src/guide.html", "w", encoding="utf-8").write(guide)
open("src/travel.html", "w", encoding="utf-8").write(travel)
print("guide", len(guide), "travel", len(travel))
