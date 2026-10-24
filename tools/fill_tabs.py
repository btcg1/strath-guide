"""Fill the Food and Shopping templates and add the apps checklist to School. One-time patch.
Facts checked 25 Oct 2026; see the Sources list (tools/build.py) for the pages."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
L = json.load(open("data/links.json", encoding="utf-8"))
moved = open(".taste-skill/moved.html", encoding="utf-8").read()
eat = moved[moved.index('<section class="food" id="food">'):moved.index("</section>") + len("</section>")]

# ---- Food: where we ate (moved from School, addresses fixed, wording tidied) ----
eat = eat.replace('<section class="food" id="food">', '<section class="food" id="eat">')
EAT_EDITS = [
 ("Honestly, you don't come to the UK for the food. The Middle Eastern and Indian food, on the other hand, is top tier. We tried everything here ourselves, so this is just our take.",
  "British food is not the reason to come, but Glasgow's Middle Eastern and Indian restaurants are excellent. We ate at every place on these lists ourselves."),
 ("George St. Full Scottish breakfast; the whole stretch near campus has cheap deals.", "92 George St. A full Scottish breakfast. The cafés along George St near campus all do cheap breakfast deals."),
 ("273 High St. Cash only, authentic, 10% off the main menu if you say you're a student.", "273 High St. Home-style Chinese food. Cash only, and 10% off the main menu if you say you're a student."),
 ("80 West Nile St. Proper, filling curry for £5–6. One of our best cheap eats.", "80 West Nile St. A filling curry for £5–6, one of the best-value meals we found."),
 ("186 London Rd, by the Barras. Top tier and reasonably priced.", "186 London Rd, by the Barras. Very good shawarma at fair prices."),
 ("Cathedral St. Cooked and served by culinary students, like the restaurant at Temasek Poly.", "190 Cathedral St. Cooked and served by culinary students, like the training restaurant at Temasek Poly."),
 ("Merchant City. Swiss food from a converted police box. Cute place, decent food.", "64a Wilson St, Merchant City. Raclette sandwiches and zapiekanka, a Polish open baguette."),
 ("Hope St. About £5. Cheap, good falafel, and vegetarian friendly.", "116 Sauchiehall St, at the top of Hope St. A good falafel wrap for about £5, and vegetarian friendly."),
 ("94 Miller St. Might be the best pizza in Glasgow.", "94 Miller St. Possibly the best pizza in Glasgow."),
 ("64 Albion St. Scottish food made with really good ingredients.", "64 Albion St. Scottish dishes made with very good ingredients."),
 ("1 MacFarlane St. Worth going for the name alone.", "1 MacFarlane St, by the Barrowland. Good Chinese food, and a name you won't forget."),
 ("65 St Vincent St. Huge burgers, so go hungry.", "65 St Vincent St. Very large burgers."),
 ("St Enoch Centre. Weekday lunch is worth it; quality is mid, but the variety is huge.", "St Enoch Centre. Weekday lunch is the best value. The cooking is average, but the choice is huge."),
 ("56 Ingram St. Our one pricier pick: a very good Sunday roast close to school.", "56 Ingram St. Our one pricier pick: a very good Sunday roast close to campus."),
 ("The Counting House, George Square. At this point it's a UK cultural experience: mid food, decent prices, different deals every day.", "The Counting House, George Square. A British institution: average food, low prices and a different deal every day."),
 ("Same menu as Singapore, but better here by far.", "The same menu as in Singapore, but noticeably better here."),
 ("Renfrew St. Glasgow has loads of brunch spots in the centre and West End.", "Renfrew St. Glasgow has plenty of brunch places in the centre and the West End."),
 ("Gibson St. We don't see Lebanese food as often in Singapore, so give it a go.", "Gibson St. Lebanese food is harder to find in Singapore, so try it here."),
 ("<td>Stack &amp; Still</td><td>Sweet and savoury pancakes.</td>", '<td><a href="https://stackandstill.co.uk/">Stack &amp; Still</a></td><td>Sweet and savoury pancakes.</td>'),
 ("Craving Chinese food and don't want to cook? Try the West End.", "For Chinese food without cooking, head to the West End."),
 ("Bank St. Very famous; worth it if you're a foodie.", "North Bank St. Famous for mash with toppings, and worth the queue."),
 ("Victoria St. Might be the best fish and chips in Scotland.", "Victoria St. Some of the best fish and chips we had in Scotland."),
]
for a, b in EAT_EDITS:
    assert a in eat, a[:50]
    eat = eat.replace(a, b)

A = lambda u, t: f'<a href="{u}">{t}</a>'
FOOD = f'''<section class="intro intro--who" aria-label="About this page">
  <p class="intro__lead" data-reveal>Menu prices in Glasgow look like Singapore's, but they are in pounds.</p>
  <div class="intro__cols">
    <p>At about S$1.70 to the pound, a £15 main costs more than S$25. Most of us cooked on weekdays and ate out at weekends, with meal deals and Too Good To Go bags for busy days. Groceries and meal deals are on the {A("shopping.html", "Shopping tab")}.</p>
    <p>We ate at every restaurant in the first lists ourselves. The Asian restaurants, student discounts and rules further down come from our own research in October 2026. Restaurants open and close quickly, so check before you go.</p>
  </div>
</section>

{eat}

<section class="tsec" id="asian">
  <h2 class="h2 tsec__title">When you miss home</h2>
  <div class="tsec__body">
    <p class="tsec__lead">Friends Chinese Café and Ho Lee Fook are above. These are the other Asian restaurants near campus with good reviews when we checked. For ingredients to cook yourself, go to Chung Ying on Dobbie's Loan (see the {A("shopping.html#asian", "Shopping tab")}).</p>
    <table class="rows rows--notes">
      <tr><td>Dim sum</td><td>{A("https://www.tripadvisor.com/Restaurant_Review-g186534-d3847134-Reviews-Loon_Fung_Restaurant-Glasgow_Scotland.html", "Loon Fung")}</td><td>417 Sauchiehall St. A Cantonese restaurant that has been open for over 50 years. Dim sum and roast duck.</td></tr>
      <tr><td>Ramen</td><td>{A("https://www.makiramen.com/our-venues/glasgow/", "Maki &amp; Ramen")}</td><td>Bath St and Renfield St. Ramen and sushi, a short walk from campus.</td></tr>
      <tr><td>Korean</td><td>{A("https://bibimbapglasgow.co.uk/", "Bibimbap")}</td><td>City centre. Stone-pot bibimbap and Korean fried chicken.</td></tr>
    </table>
  </div>
</section>

<section class="menu" id="scottish">
  <h2 class="h2 menu__title">Scottish food to try once</h2>
  <ul class="menu__pics">
    <li><figure data-large="{{{{SCOT_HAGGIS_L}}}}"><img src="{{{{SCOT_HAGGIS}}}}" alt="Haggis, neeps and tatties" width="640" height="800" loading="lazy"></figure><h3 class="menu__dish">Haggis, neeps and tatties</h3><p>Sheep's offal, oats and spices, with mashed turnip and potato. Try it at least once; some of us loved it.</p></li>
    <li><figure data-large="{{{{SCOT_FISH_L}}}}"><img src="{{{{SCOT_FISH}}}}" alt="Fish and chips, Portree" width="640" height="800" loading="lazy"></figure><h3 class="menu__dish">Fish supper</h3><p>At a chippy, "supper" means it comes with chips. Sauces and sides cost extra, so a full meal can pass £20.</p></li>
    <li><figure data-large="{{{{SCOT_STP_L}}}}"><img src="{{{{SCOT_STP}}}}" alt="Sticky toffee pudding" width="640" height="800" loading="lazy"></figure><h3 class="menu__dish">Sticky toffee pudding</h3><p>Date sponge soaked in toffee sauce. Our favourite British dessert.</p></li>
    <li><figure data-large="{{{{SCOT_ROAST_L}}}}"><img src="{{{{SCOT_ROAST}}}}" alt="Roast with Yorkshire pudding, Arbroath" width="640" height="800" loading="lazy"></figure><h3 class="menu__dish">Sunday roast</h3><p>Roast meat, potatoes, vegetables, gravy and a Yorkshire pudding. Have it at a carvery or a good steakhouse.</p></li>
  </ul>
  <ul class="menu__list">
    <li><h3 class="menu__dish">Cullen skink</h3><p>A thick soup of smoked haddock, potato and onion.</p></li>
    <li><h3 class="menu__dish">Pies</h3><p>Steak and ale pie, shepherd's pie, and the Scotch pie: a small round mutton pie sold at bakeries.</p></li>
    <li><h3 class="menu__dish">Irn-Bru</h3><p>Scotland's bright orange soft drink. Every shop sells it.</p></li>
    <li><h3 class="menu__dish">Deep-fried Mars bar</h3><p>If you dare. Our group was very split on this one.</p></li>
  </ul>
</section>

<section class="tsec" id="deals">
  <h2 class="h2 tsec__title">Markets and student deals</h2>
  <div class="tsec__body">
    <p class="tablename">Markets</p>
    <table class="rows rows--notes">
      <tr><td>Weekend market</td><td>{A("https://market.barrowland.co.uk/blogs/the-barras/opening-times", "The Barras")}</td><td>Gallowgate. Every Saturday and Sunday, 10am to 4pm. Bargains, second-hand stalls and food, with Rosto Shawarma round the corner.</td></tr>
      <tr><td>Street food</td><td>{A("https://www.spottedbylocals.com/glasgow/the-platform-at-argyle-st/", "Platform")}</td><td>Under Central Station, in the Argyle Street Arches. Street-food stalls from Friday to Sunday.</td></tr>
    </table>
    <p class="tablename">Student discounts</p>
    <table class="rows rows--notes">
      <tr><td>Japanese-style</td><td>{A("https://www.studentbeans.com/student-discount/uk/wagamama", "Wagamama")}</td><td>20% off food and drink from Sunday to Thursday with Student Beans.</td></tr>
      <tr><td>Bakery</td><td>{A("https://www.studentbeans.com/student-discount/uk/greggs", "Greggs")}</td><td>A free sausage roll with a cold Sandwich Deal with Student Beans.</td></tr>
      <tr><td>Chinese</td><td>Friends Chinese Café</td><td>10% off the main menu if you say you're a student.</td></tr>
    </table>
    <p class="tsec__note">{A("https://www.studentbeans.com/uk", "Student Beans")} is free. You verify once with your Strathclyde email, then show the code or the app at the till.</p>
  </div>
</section>

<section class="tsec" id="rules">
  <h2 class="h2 tsec__title">Tipping, water and drinks</h2>
  <div class="tsec__body">
    <dl class="facts">
      <div><dt>Tipping</dt><dd>Not expected at counters, cafés or pubs. For table service, about 10% is usual if the bill has no service charge. Some restaurants add a discretionary service charge of 10–12.5%; you can ask for it to be removed.</dd></div>
      <div><dt>Tap water</dt><dd>Free. Ask for "tap water" or you may be sold a bottle.</dd></div>
      <div><dt>Buying alcohol</dt><dd>Shops in Scotland can only sell alcohol between 10am and 10pm, and there is a {A("https://www.mygov.scot/minimum-unit-price-alcohol", "minimum price of 65p per unit")}. Shops and bars ask anyone who looks under 25 for ID, so carry your passport.</dd></div>
    </dl>
  </div>
</section>
'''

# ---- Shopping ----
SHOP = f'''<section class="intro intro--who" aria-label="About this page">
  <p class="intro__lead" data-reveal>Everything you need for a semester in halls is within walking distance of campus.</p>
  <div class="intro__cols">
    <p>Aldi on High Street is a short walk away, and the St Enoch Centre and Argyle Street have the rest. Get the loyalty apps on your first day: the lower price on many shelf labels is for members only.</p>
    <p>Shops in Scotland have {A("https://www.gov.uk/trading-hours-for-retailers-the-law", "no Sunday trading limits")}, so big stores open on Sundays too. Prices below were checked in October 2026.</p>
  </div>
</section>

<section class="tsec" id="groceries">
  <h2 class="h2 tsec__title">Supermarkets near campus</h2>
  <div class="tsec__body">
    <table class="rows rows--notes">
      <tr><td>Cheapest</td><td>Aldi</td><td>High St, a short walk from campus. The cheapest for basics. Aldi has no loyalty card.</td></tr>
      <tr><td>Better range</td><td>Lidl</td><td>Duke St, a longer walk east than Aldi, but better products. Get the {A("https://www.lidl.co.uk/c/lidl-plus/s10023095", "Lidl Plus")} app for weekly coupons.</td></tr>
      <tr><td>Everywhere</td><td>Tesco Express</td><td>Several in the centre. Prices with a {A("https://www.tesco.com/clubcard/", "Clubcard")} are often lower than the shelf price.</td></tr>
      <tr><td>Everywhere</td><td>Sainsbury's Local</td><td>Several in the centre. {A("https://www.nectar.com/nectar-prices", "Nectar Prices")} are lower prices on selected items for Nectar members.</td></tr>
      <tr><td>Everywhere</td><td>Co-op</td><td>{A("https://www.coop.co.uk/membership", "Membership")} costs £1, and you get the £1 back on your first shop.</td></tr>
      <tr><td>Toiletries</td><td>Savers</td><td>Big brands like Pantene, Dove and TRESemmé for very little.</td></tr>
      <tr><td>Cheapest of all</td><td>Poundland</td><td>Basics at the lowest prices.</td></tr>
    </table>
  </div>
</section>

<section class="mealdeal" id="mealdeals">
  <h2 class="h2 mealdeal__title">Meal deals</h2>
  <p class="mealdeal__lead">A main, a snack and a drink for one price. Prices from {A("https://www.studentbeans.com/blog/uk/best-supermarket-meal-deals-in-the-uk", "Student Beans")}, 11 August 2026.</p>
  <ol class="dots" aria-label="Meal deal prices, standard and with a loyalty card">
    {{{{MEALDEAL_ROWS}}}}
  </ol>
  <ul class="mealdeal__notes">
    <li><b>Tesco</b> had the best quality of the ones we tried.</li>
    <li><b>Co-op</b>: take the Ginsters Cornish pasty as your snack. It is as filling as a main.</li>
    <li><b>Boots</b> in Buchanan Galleries also has a clearance shelf.</li>
    <li><b>Greggs</b> gives a free sausage roll with a cold Sandwich Deal if you show {A("https://www.studentbeans.com/student-discount/uk/greggs", "Student Beans")}.</li>
    <li><b>M&amp;S</b> is the more expensive option.</li>
  </ul>
</section>

<section class="tsec" id="asian">
  <h2 class="h2 tsec__title">Asian groceries</h2>
  <div class="tsec__body">
    <table class="rows rows--notes">
      <tr><td>Chinese supermarket</td><td>{A("https://www.orientalstoredirectory.co.uk/stores/chung-ying", "Chung Ying")}</td><td>254 Dobbie's Loan, near Glasgow Caledonian University. Pricier than the supermarkets, but it has the sauces, noodles, rice and snacks you will miss. For us it was worth it.</td></tr>
    </table>
  </div>
</section>

<section class="tsec" id="firstweek">
  <h2 class="h2 tsec__title">Your first week in halls</h2>
  <div class="tsec__body">
    <table class="rows rows--notes">
      <tr><td>Kitchen and bedding</td><td>{A("https://st-enoch.com/directory/tj-hughes", "TJ Hughes")}</td><td>Ground floor of the St Enoch Centre. Cookware, bed sheets, blankets and laundry baskets. Share an Uber back to halls; split four ways it is cheap.</td></tr>
      <tr><td>Towels and basics</td><td>{A("https://www.primark.com/en-gb/stores/glasgow/56-68-argyle-street", "Primark")}</td><td>56–68 Argyle St. Cheap towels, bedding, clothes and shoes.</td></tr>
      <tr><td>Free</td><td>Leftovers from the last residents</td><td>Halls usually have a pile or a market of things previous students left behind. Check it before you buy anything.</td></tr>
    </table>
  </div>
</section>

<section class="tsec" id="clothes">
  <h2 class="h2 tsec__title">Winter clothes and outdoor gear</h2>
  <div class="tsec__body">
    <table class="rows rows--notes">
      <tr><td>Thermals</td><td>{A("https://st-enoch.com/directory/uniqlo", "Uniqlo")}</td><td>St Enoch Centre, open since October 2025. An Extra Warm Heattech inner layer got us through the winter.</td></tr>
      <tr><td>Cheap layers</td><td>Primark</td><td>Argyle St. Thermals, gloves, hats and scarves.</td></tr>
      <tr><td>Hiking gear</td><td>Mountain Warehouse</td><td>Waterproof jackets and walking boots for the Highlands.</td></tr>
      <tr><td>Second-hand</td><td>{A("https://market.barrowland.co.uk/blogs/the-barras/opening-times", "The Barras")}</td><td>Weekend market in the East End, Saturdays and Sundays from 10am to 4pm.</td></tr>
    </table>
  </div>
</section>

<section class="tsec" id="saving">
  <h2 class="h2 tsec__title">Saving money</h2>
  <div class="tsec__body">
    <dl class="facts">
      <div><dt>Too Good To Go</dt><dd>Cafés, bakeries and supermarkets sell their unsold food at closing time in surprise bags, at {A("https://www.toogoodtogo.com/en-gb", "half price or less")}. This saved us a lot of money.</dd></div>
      <div><dt>Olio</dt><dd>{A("https://olioapp.com", "A free app")} where neighbours and shops give away food and household items.</dd></div>
      <div><dt>Bags</dt><dd>Every shop in Scotland {A("https://www.mygov.scot/carrier-bag-charge", "charges at least 10p")} for a carrier bag, so keep a tote bag with you.</dd></div>
      <div><dt>Pharmacy</dt><dd>Boots and Superdrug both have several branches in the centre. Pharmacists can advise on minor illnesses without an appointment.</dd></div>
    </dl>
  </div>
</section>
'''

# ---- School: apps checklist ----
APPS = f'''<section class="apps" id="apps">
  <h2 class="h2 apps__title">Apps to download</h2>
  <p class="apps__lead">Install these in roughly this order. Links go to each app's own page.</p>
  <div class="apps__cols">
    <div class="apps__col"><h3 class="apps__when">Before you fly</h3><ul class="apps__list">
      <li>{A("https://www.strath.ac.uk/studywithus/mobileapp/", "StrathApp")}<span>Your digital student card, timetable and Myplace, Strathclyde's course site.</span></li>
      <li>{A("https://www.railcard.co.uk/16-25-railcard/", "Railcard")}<span>Buy the railcard on your phone for a third off train fares.</span></li>
      <li>{A("https://www.scotrail.co.uk/plan-your-journey/scotrail-app", "ScotRail")}<span>Train times and tickets in Scotland.</span></li>
      <li>{A("https://www.you.co", "YouTrip")} or {A("https://wise.com/gb/", "Wise")}<span>Pay in pounds from a Singapore account at a fair exchange rate.</span></li>
      <li>{A("https://www.uber.com/gb/en/", "Uber")}<span>For the airport and the first big shop.</span></li>
    </ul></div>
    <div class="apps__col"><h3 class="apps__when">In your first week</h3><ul class="apps__list">
      <li>{A("https://www.toogoodtogo.com/en-gb", "Too Good To Go")}<span>Unsold food from cafés and bakeries at half price or less.</span></li>
      <li>{A("https://www.lidl.co.uk/c/lidl-plus/s10023095", "Lidl Plus")}, {A("https://www.tesco.com/clubcard/", "Tesco Clubcard")}, {A("https://www.coop.co.uk/membership", "Co-op")}<span>Member prices, including cheaper meal deals. See the <a href="shopping.html">Shopping tab</a>.</span></li>
      <li>{A("https://www.firstbus.co.uk/greater-glasgow/tickets/ps2-fare-cap", "First Bus")}<span>Glasgow buses. Single fares are capped at £2.</span></li>
      <li>{A("https://www.strath.ac.uk/strathclydesport/mobileapp/", "Strathclyde Sport")}<span>Book gym and classes. Membership is free if you live in halls.</span></li>
      <li>{A("https://www.studentbeans.com/uk", "Student Beans")}<span>Student discounts at shops and restaurants.</span></li>
      <li>{A("https://splitwise.com/", "Splitwise")}<span>Track who owes what for shared groceries and trips.</span></li>
    </ul></div>
    <div class="apps__col"><h3 class="apps__when">Once you start travelling</h3><ul class="apps__list">
      <li>{A(L["ryanair_esn"] if "ryanair_esn" in L else "https://www.esncard.org/ryanair", "Ryanair")}<span>Cheap flights; the ESNcard gives 15% off some of them.</span></li>
      <li>{A("https://www.hostelworld.com/", "Hostelworld")}<span>Hostels for weekend trips.</span></li>
      <li>{A("https://www.ember.to/", "Ember")}<span>Electric coaches, including to Fort William through Glencoe.</span></li>
      <li>{A("https://www.metoffice.gov.uk/", "Met Office")}<span>The UK weather service. Check it before every hike.</span></li>
      <li>{A("https://aurorawatch.lancs.ac.uk/", "AuroraWatch UK")}<span>Free alerts when the northern lights might be visible.</span></li>
    </ul></div>
  </div>
</section>

'''

for name, body in (("food", FOOD), ("shopping", SHOP)):
    p = f"src/{name}.html"; s = open(p, encoding="utf-8").read()
    assert "<!--MAIN-->" in s
    open(p, "w", encoding="utf-8").write(s.replace("<!--MAIN-->", body))

g = open("src/guide.html", encoding="utf-8").read()
g = g.replace('<section class="mae" id="mae">', '<section class="tsec" id="mae">').replace('class="h2 mae__title"', 'class="h2 tsec__title"') \
     .replace('class="mae__body"', 'class="tsec__body"').replace('class="mae__lead"', 'class="tsec__lead"').replace("rows--mae", "rows--wide")
anchor = '<section class="faq" id="faq">'
assert anchor in g and 'id="apps"' not in g
g = g.replace(anchor, APPS + anchor, 1)
g = g.replace('<a href="#costs">Costs</a><a href="#faq">FAQ</a>', '<a href="#costs">Costs</a><a href="#apps">Apps</a><a href="#faq">FAQ</a>', 1)
open("src/guide.html", "w", encoding="utf-8").write(g)
print("filled food, shopping, apps")
