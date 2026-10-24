"""Patch tools/build.py: two pages, guide strip, links in panels and the places index."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "tools", "build.py"); s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80]); s = s.replace(a, b)

rep('R["STRIP_CAPTION0"] = esc(picks["strip"][0]["cap"])',
    'R["STRIP_CAPTION0"] = esc(picks["strip"][0]["cap"])\n'
    'L = json.load(open(J("data", "links.json"), encoding="utf-8"))\n'
    'A = lambda key, text: f\'<a href="{L[key]}">{text}</a>\'\n'
    'gstr = []\n'
    'for i, s_ in enumerate(picks["gstrip"]):\n'
    '    wsrc, ww, wh = export(s_["file"], f"gstrip/{i}-w.jpg", 5.0, (1600, 320), s_["y"])\n'
    '    msrc, mw, mh = export(s_["file"], f"gstrip/{i}-m.jpg", 2.0, (1000, 500), s_["y"])\n'
    '    gstr.append(f\'<img class="{"is-on" if i == 0 else ""}" src="{wsrc}" data-mobile="{msrc}" data-cap="{esc(s_["cap"])}" alt="{esc(s_["cap"])}" width="{ww}" height="{wh}"{"" if i == 0 else " loading=\\"lazy\\""}>\')\n'
    'R["G_STRIP_IMGS"] = "\\n          ".join(gstr)\n'
    'R["G_STRIP0"] = "photos/gstrip/0-w.jpg"\n'
    'R["G_STRIP_CAPTION0"] = esc(picks["gstrip"][0]["cap"])')

rep('''("apply", "Apply", "<p>Through NTU's GEM Explorer. You need''', '''("apply", "Apply", f"<p>Through NTU's {A('gem_explorer', 'GEM Explorer')}, on the {A('gem_portal', 'GEM Mobility Portal')}. You need''')
rep("<li>Strathclyde takes nominations 1 March", "<li>{A('strath_partners', 'Strathclyde takes nominations')} 1 March")
rep("takes nominations')} 1 March – 15 May", "takes nominations')} 1 March – 15 May")
rep('''("match", "Match", "<p>Find past matches in CourseFinder, then submit each one in NTU's online course matching system.</p><ul><li>Strathclyde's rule:''',
    '''("match", "Match", f"<p>Find past matches in {A('coursefinder', 'CourseFinder')}, then submit each one in NTU's {A('coursematching', 'online course matching system')} (both need your NTU login).</p><ul><li>Pick classes from Strathclyde's {A('strath_classes', 'exchange class catalogue')}.</li><li>{A('strath_choosing', "Strathclyde's rule")}:''')
rep('''("fly", "Fly", "<p>Get a UK ETA first: £20 on GOV.UK''', '''("fly", "Fly", f"<p>Get a {A('eta', 'UK ETA')} first: £20 on GOV.UK''')
rep("<li>You enter as a Standard Visitor:", "<li>You enter as a {A('visit_study', 'Standard Visitor')}:")
rep("<li>NTU first: briefing, indemnity letter, ISOS app, Travel Registry.</li>",
    "<li>NTU first: briefing, indemnity letter, ISOS app, {A('ntu_predep', 'Travel Registry')}. Then {A('mfa_eregister', 'eRegister with MFA')}.</li>")
rep('''("settle", "Settle", "<p>Airport Express 500 to Buchanan''', '''("settle", "Settle", f"<p>{A('airport500', 'Airport Express 500')} to Buchanan''')
rep("<li>Week one: UK SIM, Railcard, Monzo, ESNcard at the society fair (it sells out).</li>",
    "<li>Week one: {A('lebara', 'UK SIM')}, {A('railcard1625', 'Railcard')}, {A('monzo', 'Monzo')}, {A('esncard', 'ESNcard')} at the society fair (it sells out).</li>")

# places: official page per row, and links in the group notes
LINKS = {"Glencoe": "ember", "Glenfinnan": "glenfinnan", "Loch Ness": "urquhart", "Dunkeld & Birnam": "hermitage", "Oban": "staffa",
         "Stirling": "stirling_castle", "Falkirk": "falkirk_wheel", "New Lanark": "newlanark", "Dunnottar Castle": "dunnottar",
         "East Linton & Preston Mill": "prestonmill", "Linlithgow": "linlithgow", "Isle of Arran": "calmac_arran", "Inchcolm Island": "maidoftheforth",
         "Puffins & North Berwick": "seabird", "Isle of May": "isleofmay", "Shetland": "northlink", "St Andrews": "standrews_castle", "Culross": "culross",
         "Anstruther & Fife Coastal Path": "dayrider", "Edinburgh": "edinburgh_castle", "Giant's Causeway & Belfast": "belfast923",
         "West End & Kelvingrove": "kelvingrove", "Cathedral & Necropolis": "necropolis", "Pollok Park & the Burrell": "burrell",
         "Hunterian Museum": "hunterian", "City Chambers": "citychambers", "Tennent's Brewery": "tennents"}
rep("groups, count = [], 0", f"PLACE_LINK = {LINKS!r}\nNOTE = {{'Weekend tours': lambda t: t.replace('ESN Strathclyde', A('esn_strath', 'ESN Strathclyde')), 'By train': lambda t: t.replace('ScotRail', A('scotrail', 'ScotRail')).replace('A Railcard', 'A ' + A('railcard1625', 'Railcard')), 'By bus': lambda t: t.replace('Stagecoach East Scotland DayRider', A('dayrider', 'Stagecoach East Scotland DayRider')), 'By coach': lambda t: t.replace('Flixbus', A('flixbus', 'Flixbus')).replace('Student Beans', A('flix_sb', 'Student Beans'))}}\ngroups, count = [], 0")
rep('''        lis.append(f'<li class="index__row" tabindex="0"{prev}>{thumb}<span class="index__name">{esc(name)}</span><span class="index__info">{info}</span></li>')''',
    '''        nm = f'<a class="index__name" href="{L[PLACE_LINK[name]]}">{esc(name)}</a>' if name in PLACE_LINK else f'<span class="index__name">{esc(name)}</span>'
        ti = '' if name in PLACE_LINK else ' tabindex="0"'
        lis.append(f'<li class="index__row"{ti}{prev}>{thumb}{nm}<span class="index__info">{info}</span></li>')''')
rep('''    groups.append(f'<div class="index__group"><h3>{esc(title)}</h3><p>{esc(note)}</p><ul class="index__list">{"".join(lis)}</ul></div>')''',
    '''    groups.append(f'<div class="index__group"><h3>{esc(title)}</h3><p>{NOTE.get(title, lambda t: t)(esc(note))}</p><ul class="index__list">{"".join(lis)}</ul></div>')''')

# render both pages
rep('''page = open(J("src", "template.html"), encoding="utf-8").read()
for k, v in R.items():
    page = page.replace("{{" + k + "}}", v)
left = re.findall(r"\\{\\{[A-Z0-9_]+\\}\\}", page)
assert not left, left
open(J("index.html"), "w", encoding="utf-8").write(page)''',
'''for src_name, out_name in (("guide.html", "index.html"), ("travel.html", "travel.html")):
    page = open(J("src", src_name), encoding="utf-8").read()
    for k, v in R.items():
        page = page.replace("{{" + k + "}}", v)
    left = re.findall(r"\\{\\{[A-Z0-9_]+\\}\\}", page)
    assert not left, (src_name, left)
    open(J(out_name), "w", encoding="utf-8").write(page)''')
rep('print(f"index.html written.', 'print(f"index.html + travel.html written.')
open(p, "w", encoding="utf-8").write(s)
print("build.py patched")
