"""Photos tab (user: "camera roll can be a seperate tab. This time include more pics of each place i went").
Creates src/photos.html, moves the camera roll off the Travel tab, and adds the tab to every page. One-time."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = "https://btcg1.github.io/strath-guide/"

def sub(s, a, b):
    assert a in s, a[:70]; return s.replace(a, b, 1)

# every page gets the fifth tab
for name in ("guide", "food", "shopping", "travel"):
    p = f"src/{name}.html"; s = open(p, encoding="utf-8").read()
    s = re.sub(r'(<a href="travel.html"( aria-current="page")?>Travel</a>)</div>', r'\1<a href="photos.html">Photos</a></div>', s, count=1)
    assert 'href="photos.html">Photos</a>' in s, name
    open(p, "w", encoding="utf-8").write(s)

t = open("src/travel.html", encoding="utf-8").read()
roll = t[t.index('<section class="roll" id="photos">'):]
roll = roll[:roll.index("</section>") + len("</section>")]
extra = t[t.index('<section class="extra" id="extra">'):]
extra = extra[:extra.index("</section>") + len("</section>")]
t = t.replace(roll + "\n", "").replace(extra + "\n", "")
t = sub(t, '<a href="#places">Places</a><a href="#photos">Photos</a><a href="#extra">Wales</a></div>', '<a href="#places">Places</a><a href="#questions">FAQ</a></div>')
t = sub(t, "Here's our map of 24 trips, plus 36 places with prices and opening times, and photos from along the way.",
        "Here's our map of 24 trips, plus 36 places with prices and opening times. The photos have their own tab.")
open("src/travel.html", "w", encoding="utf-8").write(t)

# the Photos page: head, nav and footer from the Travel template
head = t[:t.index("<body>")]
desc = "Our camera roll from a semester at Strathclyde: the best photos from every trip, in date order."
head = re.sub(r"<title>.*?</title>", "<title>Photos – Strath Field Guide</title>", head)
head = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + desc, head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>Photos – Strath Field Guide", head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + desc, head)
head = head.replace(SITE + "travel.html", SITE + "photos.html").replace("photos/og/travel.jpg", "photos/og/pstrip.jpg").replace("{{STRIP0}}", "{{P_STRIP0}}")
nav = t[t.index('<nav class="topnav"'):t.index("</nav>") + len("</nav>")]
nav = nav.replace(' aria-current="page"', "").replace('<a href="photos.html">Photos</a>', '<a href="photos.html" aria-current="page">Photos</a>')
nav = re.sub(r'<div class="topnav__links">.*?</div>', '<div class="topnav__links"><a href="#trips">Trips</a><a href="#roll">Album</a></div>', nav)
foot = t[t.index("<footer"):]
foot = re.sub(r'<p class="foot__invite">.*?</p>', '<p class="foot__invite">See you in&nbsp;Glasgow</p>', foot, 1)
foot = re.sub(r"<script>window\.TRIPS.*?</script>\n", "", foot)
foot = foot.replace("<span>Map outline: Natural Earth.</span>", "")
roll = roll.replace('<section class="roll" id="photos">', '<section class="roll" id="roll">').replace("{{WALL}}", "{{ROLL}}")
page = head + "<body>\n" + nav + """
<header class="hero" id="top">
  <div class="hero__body">
    <h1 class="hero__title">
      <span class="hero__line"><span class="hero__word">Camera</span></span>
      <span class="hero__line hero__line--2"><span class="hero__word">roll</span></span>
    </h1>
    <div class="hero__pitch">
      <p class="hero__lead">{{ROLL_COUNT}} photos from {{ROLL_TRIPS}} trips, picked for composition from the {{ROLL_ALL}} we took. In date order, Glasgow first.</p>
      <div class="hero__actions"><a class="button" href="#trips">Pick a trip</a><a class="hero__alt" href="travel.html">Trips and places</a></div>
    </div>
    <figure class="hero__frame"><span class="strip shutter" data-strip>
          {{P_STRIP_IMGS}}
        </span><figcaption class="hero__photo">In the photo: <span data-strip-caption>{{P_STRIP_CAPTION0}}</span></figcaption></figure>
  </div>
</header>

<main>
<section class="tripjump" id="trips" aria-label="Trips">
  <ol class="tripjump__list">
    {{ROLL_INDEX}}
  </ol>
</section>

""" + roll + "\n</main>\n\n" + foot
open("src/photos.html", "w", encoding="utf-8").write(page)
open(".taste-skill/extra_section.html", "w", encoding="utf-8").write(extra)
print("photos tab created; travel roll + extra removed")
