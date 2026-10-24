"""Create src/food.html and src/shopping.html shells from the Travel template (head, nav, hero, footer). One-time.
The main content goes where <!--MAIN--> sits."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = "https://btcg1.github.io/strath-guide/"
t = open("src/travel.html", encoding="utf-8").read()
head = t[:t.index("<header")]
foot = t[t.index("<footer"):]

PAGES = {
 "food": dict(file="food.html", title="Food – Strath Field Guide",
     desc="Where we ate in Glasgow and around Scotland, what it cost, the Scottish dishes worth trying, student discounts and how tipping works.",
     strip="F", words=("Eating out in", "Glasgow"), links=[("#eat", "Glasgow"), ("#scottish", "Scottish food"), ("#deals", "Deals")],
     lead="Where we ate, what it cost and what we'd order again, plus the Scottish dishes worth trying at least once.",
     cta=("#eat", "See where we ate"), alt=("shopping.html", "Groceries and shopping"),
     invite="Then do a big&nbsp;shop", next=("shopping.html", "Groceries and shopping")),
 "shopping": dict(file="shopping.html", title="Shopping – Strath Field Guide",
     desc="Supermarkets near Strathclyde and their apps, Asian groceries, meal deals, first-week shopping for halls, winter clothes and pharmacies.",
     strip="S", words=("Stocking up in", "Glasgow"), links=[("#groceries", "Groceries"), ("#firstweek", "First week"), ("#clothes", "Clothes")],
     lead="Which supermarkets are close to campus, which loyalty apps are worth having, and where to buy everything else you need for a semester in halls.",
     cta=("#groceries", "Start with groceries"), alt=("food.html", "Eating out"),
     invite="Then go and see&nbsp;Scotland", next=("travel.html", "Trips and places")),
}
for key, p in PAGES.items():
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + p["desc"], h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + p["title"], h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + p["desc"], h)
    h = h.replace(SITE + "travel.html", SITE + p["file"]).replace("photos/og/travel.jpg", f"photos/og/{p['strip'].lower()}strip.jpg")
    h = h.replace("{{STRIP0}}", "{{" + p["strip"] + "_STRIP0}}")
    tabs = '<div class="tabs" aria-label="Pages">' + "".join(
        f'<a href="{f}"{" aria-current=\"page\"" if f == p["file"] else ""}>{n}</a>'
        for f, n in [("index.html", "School"), ("food.html", "Food"), ("shopping.html", "Shopping"), ("travel.html", "Travel")]) + "</div>"
    links = "".join(f'<a href="{a}">{n}</a>' for a, n in p["links"])
    s = p["strip"]
    body = f"""<body>
<header class="hero" id="top">
  <nav class="topnav" aria-label="Main">
    <a class="wordmark" href="index.html">Strath Field Guide</a>
    {tabs}
    <div class="topnav__links">{links}</div>
  </nav>
  <div class="hero__body">
    <h1 class="hero__title">
      <span class="hero__line"><span class="hero__word">{p['words'][0]}</span>
        <span class="stripwrap"><span class="strip shutter" data-strip>
          {{{{{s}_STRIP_IMGS}}}}
        </span></span></span>
      <span class="hero__line hero__line--2"><span class="hero__word">{p['words'][1]}</span></span>
    </h1>
    <div class="hero__pitch">
      <p class="hero__lead">{p['lead']}</p>
      <div class="hero__actions"><a class="button" href="{p['cta'][0]}">{p['cta'][1]}</a><a class="hero__alt" href="{p['alt'][0]}">{p['alt'][1]}</a></div>
      <p class="hero__photo">In the photo: <span data-strip-caption>{{{{{s}_STRIP_CAPTION0}}}}</span></p>
    </div>
  </div>
</header>

<main>
<!--MAIN-->
</main>

"""
    f = foot
    f = re.sub(r'<p class="foot__invite">.*?</p>', f'<p class="foot__invite">{p["invite"]}</p>', f, 1)
    f = re.sub(r'<a class="button button--light" href="[^"]*">.*?</a>', f'<a class="button button--light" href="{p["next"][0]}">{p["next"][1]}</a>', f, 1)
    f = f.replace("<span>Map outline: Natural Earth.</span>", "")
    f = re.sub(r"<script>window\.TRIPS.*?</script>\n", "", f)
    page = h + body + f
    open(f"src/{p['file']}", "w", encoding="utf-8").write(page)
    print("wrote src/" + p["file"])
