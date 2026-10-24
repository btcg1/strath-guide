"""Geocode the semester's trip places with OpenStreetMap Nominatim (1 request/second, per its usage policy)."""
import json, time, urllib.parse, urllib.request, os

PLACES = {
    "strath": "University of Strathclyde, Glasgow",
    "oban": "Oban, Argyll and Bute, Scotland",
    "york": "York, England",
    "glenfinnan": "Glenfinnan Viaduct, Scotland",
    "falkirk": "The Kelpies, Falkirk, Scotland",
    "inchcolm": "Inchcolm Abbey, Scotland",
    "lochness": "Urquhart Castle, Scotland",
    "arbroath": "Arbroath, Scotland",
    "hamilton": "Hamilton, South Lanarkshire, Scotland",
    "stirling": "Stirling Castle, Scotland",
    "skye": "Portree",
    "storr": "Old Man of Storr, Scotland",
    "culross": "Culross, Fife, Scotland",
    "dunnottar": "Dunnottar Castle, Scotland",
    "standrews": "St Andrews, Fife, Scotland",
    "arran": "Brodick, Isle of Arran, Scotland",
    "newlanark": "New Lanark, Scotland",
    "edinburgh": "Edinburgh Castle, Scotland",
    "lomond": "Balloch, West Dunbartonshire, Scotland",
    "hillhouse": "Hill House, Helensburgh",
    "aberdeen": "Footdee, Aberdeen, Scotland",
    "crathes": "Crathes Castle, Scotland",
    "prestonmill": "Preston Mill, East Linton, Scotland",
    "tantallon": "Tantallon Castle, Scotland",
    "northberwick": "North Berwick, Scotland",
    "argyll": "Glenbranter, Argyll and Bute, Scotland",
    "dunoon": "Dunoon, Scotland",
    "dunkeld": "Dunkeld, Perth and Kinross, Scotland",
    "belfast": "Belfast, Northern Ireland",
    "causeway": "Giant's Causeway, Northern Ireland",
    "derry": "Derry, Northern Ireland",
    "inverness": "Inverness, Scotland",
    "aviemore": "Aviemore, Scotland",
    "wick": "Wick, Highland, Scotland",
    "culloden": "Culloden Battlefield, Scotland",
    "chester": "Chester, England",
    "conwy": "Conwy Castle, Wales",
    "snowdonia": "Snowdon, Wales",
    "glencoe": "Glencoe, Highland, Scotland",
    "eileandonan": "Eilean Donan, Scotland",
    "kilchurn": "Kilchurn Castle, Scotland",
    "linlithgow": "Linlithgow Palace, Scotland",
    "pitlochry": "Pitlochry, Scotland",
    "corrour": "Corrour railway station, Scotland",
    "isleofmay": "Isle of May, Scotland",
    "anstruther": "Anstruther, Fife, Scotland",
    "lerwick": "Lerwick, Shetland, Scotland",
    "fortwilliam": "Fort William, Scotland",
    "pollok": "Pollok Country Park, Glasgow",
    "kelvingrove": "Kelvingrove Art Gallery and Museum, Glasgow",
    "necropolis": "Glasgow Necropolis",
    "barras": "Barras Market, Glasgow",
}
out_path = os.path.join(os.path.dirname(__file__), "..", "data", "coords.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
res = json.load(open(out_path)) if os.path.exists(out_path) else {}
for k, q in PLACES.items():
    if k in res:
        continue
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1})
    req = urllib.request.Request(url, headers={"User-Agent": "strath-field-guide/1.0 (student guide; benedict2807@gmail.com)"})
    try:
        j = json.load(urllib.request.urlopen(req, timeout=20))
        if j:
            res[k] = {"lat": round(float(j[0]["lat"]), 4), "lon": round(float(j[0]["lon"]), 4), "osm": j[0].get("display_name", "")[:80]}
        else:
            print("NOT FOUND", k, q)
    except Exception as e:
        print("FAIL", k, e)
    time.sleep(1.1)
json.dump(res, open(out_path, "w"), indent=1)
print(len(res), "places geocoded")
for k, v in res.items():
    print(f"{k:12} {v['lat']:8} {v['lon']:8}  {v['osm'][:60]}")
