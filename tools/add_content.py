"""Guide additions: dates + weather section, more FAQs, clearer hero button."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
L = json.load(open("data/links.json", encoding="utf-8"))
a = lambda k, t: f'<a href="{L[k]}">{t}</a>'
g = open("src/guide.html", encoding="utf-8").read()
def rep(x, y):
    global g
    assert g.count(x) == 1, (g.count(x), x[:80]); g = g.replace(x, y)

rep('<a class="button" href="#apply">How to apply</a>', '<a class="button" href="#apply">Read the four steps</a>')

WX = [("September", "16.1", "9.1", 113, 100), ("October", "12.4", "6.1", 81, 124), ("November", "8.9", "3.4", 50, 110), ("December", "6.4", "1.3", 33, 118),
      ("January", "6.3", "1.3", 39, 112), ("February", "7.0", "1.4", 65, 98), ("March", "9.1", "2.5", 91, 87), ("April", "12.1", "4.3", 137, 65), ("May", "15.3", "6.5", 183, 63)]
wx_rows = "".join(f'<tr><td>{m}</td><td class="n">{hi}°</td><td class="n">{lo}°</td><td><span class="sunbar" style="--v:{s / 183:.2f}"></span><span class="n">{s} h</span></td><td class="n">{r} mm</td></tr>' for m, hi, lo, s, r in WX)
DATES = f'''<section class="dates" id="dates">
  <h2 class="h2">Dates and&nbsp;weather</h2>
  <div class="dates__grid">
    <div>
      <p class="tablename">{a('strath_keydates', 'Strathclyde 2026/27')}</p>
      <table class="rows">
        <tr><td>Semester 1</td><td>Welcome week</td><td>14–20 Sep 2026</td></tr>
        <tr><td></td><td>Teaching</td><td>21 Sep – 6 Dec</td></tr>
        <tr><td></td><td>Exam timetable out</td><td>first week of Nov</td></tr>
        <tr><td></td><td>Assessments</td><td>7–18 Dec</td></tr>
        <tr class="gap"><td>Holiday</td><td>Winter vacation</td><td>19 Dec – 10 Jan</td></tr>
        <tr class="gap"><td>Semester 2</td><td>Welcome week</td><td>11–17 Jan 2027</td></tr>
        <tr><td></td><td>Teaching</td><td>18 Jan – 4 Apr</td></tr>
        <tr><td></td><td>Exam timetable out</td><td>early March</td></tr>
        <tr><td></td><td>Spring vacation</td><td>5–18 Apr</td></tr>
        <tr><td></td><td>Assessments</td><td>19 Apr – 21 May</td></tr>
      </table>
      <p class="dates__note">The dates move by a few days each year, so check the current calendar. Nominations from NTU close on 15 May for a September start and 15 October for January.</p>
    </div>
    <div>
      <p class="tablename">{a('nhs', 'Glasgow weather')} <span class="soft">(Met Office averages, 1991–2020)</span></p>
      <table class="wx2">
        <thead><tr><th>Month</th><th class="n">High</th><th class="n">Low</th><th>Sunshine</th><th class="n">Rain</th></tr></thead>
        <tbody>{wx_rows}</tbody>
      </table>
      <p class="dates__note">December gets about 33 hours of sunshine in the whole month. It rains more than 60 mm every month, so a proper waterproof matters more than a thick coat.</p>
    </div>
  </div>
</section>'''
DATES = DATES.replace(L["nhs"], "https://www.metoffice.gov.uk/research/climate/maps-and-data/location-specific-long-term-averages/gcuvzv5wy", 1)
i = g.index('<section class="costs" id="costs">'); g = g[:i] + DATES + "\n\n" + g[i:]
rep('<a href="#apply">Apply</a><a href="#costs">Costs</a><a href="#faq">FAQ</a>', '<a href="#apply">Apply</a><a href="#dates">Dates</a><a href="#costs">Costs</a><a href="#faq">FAQ</a>')

Q = lambda q, ans: f'    <details><summary>{q}</summary><div>{ans}</div></details>\n'
EXTRA = (Q("What if something goes wrong?", f"<p>Call 999 in an emergency. For urgent health advice that isn't an emergency, call NHS 24 on 111. Keep NTU's ISOS app on your phone and {a('mfa_eregister', 'eRegister with MFA')} so Singapore can reach you if something happens.</p>")
 + Q("What's the time difference with Singapore?", "<p>Singapore is 8 hours ahead of Glasgow from late October to late March, and 7 hours ahead the rest of the year, when the UK is on summer time. Plan calls home around that: lunch in Glasgow is evening in Singapore.</p>")
 + Q("Can I rent privately instead of halls?", f"<p>You can, but for one semester halls are much simpler. Halls are exempt from council tax. In a private flat, ask Strath for a student status letter for the council; whether you get the exemption is the council's decision. {a('strath_accom', 'Strath accommodation')}.</p>")
 + Q("How does the student card work?", f"<p>Most students never need a physical card: once you register, your {a('strath_card', 'digital student card')} is in the Strathclyde app. If you want a plastic one, ask at the Teaching and Learning Building (it was free when we went).</p>"))
rep('    <details><summary>Is the NHS free for me?</summary>', EXTRA + '    <details><summary>Is the NHS free for me?</summary>')
open("src/guide.html", "w", encoding="utf-8").write(g)

css = open("css/site.css", encoding="utf-8").read()
add = '''
/* Dates and weather */
.dates { padding: var(--section) var(--m) 0; }
.dates__grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: var(--gutter) calc(var(--gutter) * 3); margin-top: 72px; align-items: start; }
.dates__grid > div { display: grid; gap: 14px; min-width: 0; }
.dates__note { max-width: 50ch; }
.wx2 { width: 100%; }
.wx2 th { text-align: left; font-weight: 500; font-size: var(--step-small); color: var(--muted); padding: 0 10px 10px 0; }
.wx2 td { padding: 0 10px 12px 0; font-size: var(--step-body); }
.wx2 .n { text-align: right; font-variant-numeric: tabular-nums; }
.sunbar { display: inline-block; height: 10px; width: calc(var(--v) * 90px); background: var(--accent); margin-right: 8px; vertical-align: 0; }
@media (max-width: 860px) { .dates__grid { grid-template-columns: minmax(0, 1fr); margin-top: 40px; gap: 48px; } .wx2 td, .wx2 th { font-size: 0.9375rem; padding-right: 6px; } .sunbar { width: calc(var(--v) * 44px); } }
'''
open("css/site.css", "w", encoding="utf-8").write(css + add)
print("content added")
