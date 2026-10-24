# Strath Field Guide

A static website for NTU students going on exchange to the University of Strathclyde, Glasgow.

## Open it

Double-click `index.html`. It works straight from the folder. The map tiles, the fonts and the live exchange rate need an internet connection.

## Put it online

The site is plain HTML, CSS and JavaScript, so any static host works. Upload these:

```
index.html
css/
js/
photos/
```

Leave out `_source/`, `tools/`, `data/`, `src/` and `.taste-skill/`. They are only needed to rebuild.

- **Netlify Drop:** drag a folder holding the four items above onto https://app.netlify.com/drop.
- **GitHub Pages:** push the repo and turn on Pages for the main branch. `.gitignore` already leaves out the source photos.

## Change something

| To change | Edit | Then |
| --- | --- | --- |
| Page text, tables, FAQ | `src/template.html` | `python tools/build.py` |
| Trips on the map | `data/trips.json` (and `data/picks.json` for photos) | `python tools/build.py` |
| Places list | the `P = [...]` block in `tools/build.py` | `python tools/build.py` |
| Look and layout | `css/site.css` | refresh the browser |
| Map, exchange rate, lightbox | `js/site.js` | refresh the browser |

`tools/build.py` exports each photo for its slot from `_source/` and writes `index.html` from `src/template.html`. If you change a crop, delete that photo from `photos/` first, since existing files are kept.

## Facts

Prices, dates and opening times were checked against the official pages listed in the Sources section on 24–25 October 2026. The £→S$ rate updates live from open.er-api.com when the page opens, and falls back to 1.71 if that fails.

## Photos

All photos are the author's own (Ricoh GR, Sep–Dec 2025), resized with EXIF and GPS data removed. Photos with recognisable friends in them were left out.
