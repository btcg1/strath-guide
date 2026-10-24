"""Split the Guide page into School / Food / Shopping / Travel. One-time patch: moves sections and FAQ items, rewrites the tab bar.
Saves the food section and food/grocery FAQ items to .taste-skill/moved.html for the new templates."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
g = open("src/guide.html", encoding="utf-8").read()
t = open("src/travel.html", encoding="utf-8").read()

def cut(s, start, end="</section>\n"):
    i = s.index(start); j = s.index(end, i) + len(end)
    return s[:i] + s[j:].lstrip("\n"), s[i:j]

g, around = cut(g, '<section class="around" id="around">')
g, food = cut(g, '<section class="food" id="food">')

def take(s, q):
    m = re.search(r"    <details[^>]*><summary>" + re.escape(q) + r".*?</details>\n", s, re.S)
    assert m, q
    return s[:m.start()] + s[m.end():], m.group(0)

moved_faq = {}
for q in ["Where do I buy groceries?", "Which meal deal?", "What British food is worth ordering?",
          "How do buses work?", "Is National Trust for Scotland worth it?", "Best hikes?", "Where can I see the northern lights?"]:
    g, moved_faq[q] = take(g, q)

os.makedirs(".taste-skill", exist_ok=True)
open(".taste-skill/moved.html", "w", encoding="utf-8").write(food + "\n" + "".join(moved_faq[q] for q in ["Where do I buy groceries?", "Which meal deal?", "What British food is worth ordering?"]))

# Travel: getting around after the intro, trip questions after the places index
t = t.replace('<section class="trips" id="trips">', around + "\n" + '<section class="trips" id="trips">', 1)
travel_faq = ('<section class="faq faq--travel" id="questions">\n  <h2 class="h2 faq__title">Questions about trips</h2>\n  <div class="faq__list">\n'
              + "".join(moved_faq[q] for q in ["How do buses work?", "Is National Trust for Scotland worth it?", "Best hikes?", "Where can I see the northern lights?"])
              + "  </div>\n</section>\n\n")
t = t.replace('<section class="roll" id="photos">', travel_faq + '<section class="roll" id="photos">', 1)

def tabs(cur):
    names = [("index.html", "School"), ("food.html", "Food"), ("shopping.html", "Shopping"), ("travel.html", "Travel")]
    return '<div class="tabs" aria-label="Pages">' + "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{n}</a>' for h, n in names) + "</div>"
g = re.sub(r'<div class="tabs" aria-label="Pages">.*?</div>', tabs("index.html"), g, 1)
t = re.sub(r'<div class="tabs" aria-label="Pages">.*?</div>', tabs("travel.html"), t, 1)
t = t.replace('<div class="topnav__links"><a href="#trips">Map</a>', '<div class="topnav__links"><a href="#around">Transport</a><a href="#trips">Map</a>', 1)
open("src/guide.html", "w", encoding="utf-8").write(g)
open("src/travel.html", "w", encoding="utf-8").write(t)
print("split: around + 4 FAQ -> travel; food + 3 FAQ saved to .taste-skill/moved.html")
