# BOTW-Inspired Real-Life Cookbook Project

Working title: **The Wild Table**

This folder contains the first concrete book artifact for an unofficial, original, real-world cookbook inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim cooking.

## Files
- `data/botw_food_source_extract.json` — structured recipe catalog extracted from public wiki data for planning.
- `data/botw_food_source_extract.csv` — spreadsheet-friendly catalog.
- `data/totk_game8_recipes.json` — scraped planning reference for Tears of the Kingdom cooked dishes and elixirs from Game8, used for duplicate screening.
- `data/skyrim_uesp_cooking_recipes.json` — scraped planning reference for Skyrim player-cooked foods from UESP's MediaWiki API.
- `manuscript/The_Wild_Table_v0.5.md` — expanded literal book manuscript with the Breath of the Wild set plus non-duplicate Tears of the Kingdom additions adapted into full recipe pages.
- `manuscript/The_Wild_Table_v0.4.md` — previous draft kept for history.
- `manuscript/The_Wild_Table_v0.3.md` — previous draft kept for history.
- `manuscript/The_Wild_Table_v0.2.md` — previous draft kept for history.
- `manuscript/The_Wild_Table_v0.1.md` — previous draft kept for history.

## Current status
- Catalogued the original 116 cooking pot meals, 12 elixirs, 46 roasted foods, and 13 frozen foods, then cross-checked Tears of the Kingdom additions.
- Drafted 211 full real-life recipe pages, including 51 Skyrim player-cooked food adaptations.
- Next step: format/export the manuscript into a literal book file, then optionally design a cover and interior layout.

## Rights note
Keep the final book clearly unofficial/fan-made and use original prose, original photography/illustration, and no Nintendo-owned art/logos/screenshots.

## Book exports
- `book/The_Wild_Table.epub` — ebook version for Apple Books, Kindle conversion, Calibre, etc.
- `book/The_Wild_Table.html` — printable/styled web book version.

## GitHub Pages site
- `docs/index.html` — GitHub Pages landing page with book navigation.
- `docs/chapters/` — chapter pages split from the EPUB source.
- `docs/styles/site.css` — responsive sidebar/navigation styling.
- `docs/book/The_Wild_Table.epub` — downloadable EPUB from the site.

To publish with GitHub Pages:
1. Push this repository to GitHub.
2. In GitHub, open **Settings → Pages**.
3. Set **Source** to **Deploy from a branch**.
4. Select branch `main` and folder `/docs`.
5. Save. The site will publish at `https://<username>.github.io/<repo>/`.
