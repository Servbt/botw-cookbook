# The Wild Table — an unofficial real-world cookbook

An original, unofficial cookbook adapted from Breath of the Wild, Tears of the
Kingdom, and Skyrim cooking. 211 recipes across eight reader-facing chapters,
published as a GitHub Pages site plus a downloadable EPUB and a printable web book.

Live site: https://servbt.github.io/botw-cookbook/

## How it is built (single source of truth)

Everything is generated from one canonical model, so the manuscript, EPUB, print
edition, and website can never drift apart.

- `cookbook_model.py` — parses the manuscript into structured recipes, classifies
  them into the eight thematic chapters, applies dietary tags and voice notes.
- `cookbook_overlays.py` — authored content: bespoke Skyrim methods (replacing the
  old templated blocks) and "serving note" voice lines.
- `cookbook_build.py` — writes the manuscript (`manuscript/The_Wild_Table_v0.6.md`),
  the EPUB (`book/The_Wild_Table.epub`), and the print edition (`book/The_Wild_Table.html`).
- `cookbook_build_site.py` — writes the whole `docs/` site: hero index, chapter
  pages, filterable search, `sitemap.xml`, `robots.txt`, and a legal page.

Rebuild everything with:

```
python3 cookbook_build_site.py
pytest tests -q
```

## Chapters (reader-facing)

| Chapter | Title |
| --- | --- |
| I | Stable Comforts |
| II | Road Food: Skewers, Roasts & Grills |
| III | Rice, Curry & Village Bowls |
| IV | From the Coasts: Seafood |
| V | Sweets, Cakes & Crepes |
| VI | Elixirs & Tonics |
| VII | Tears of the Kingdom Additions |
| VIII | Skyrim: A Nord's Table |

Appendices A–D are the in-game checklists; there is also a Legal & Disclaimer page.

## Website features

- `docs/index.html` — hero landing with a pantry search box, chapter cards, contents.
- `docs/search.html` — search by the ingredients you have; filter by chapter and by
  dietary tag (vegetarian, vegan, dairy-free, gluten-free, quick, easy). Every
  result deep-links to the exact recipe.
- `docs/sitemap.xml`, `docs/robots.txt` — discovery.
- Open Graph tags on every page for nice link previews.
- Print CSS so any chapter prints cleanly, plus a one-file printable edition.

## Book exports

- `book/The_Wild_Table.epub` — ebook for Apple Books, Kindle (via Calibre), etc.
- `book/The_Wild_Table.html` — printable/save-as-PDF web book.

## Rights note

Keep this clearly unofficial and fan-made: original prose, original illustrations
and icons, and no Nintendo/Bethesda-owned art, logos, or screenshots. The site and
book both carry an explicit "not affiliated" notice.

## Publishing

GitHub Pages is served from `main` → `/docs`, so pushing to `main` updates the site.
