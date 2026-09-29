import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OEBPS = ROOT / "book" / "epub_build" / "OEBPS"
DOCS = ROOT / "docs"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def embedded_index() -> list:
    html = read(DOCS / "search.html")
    m = re.search(r'<script id="recipe-index" type="application/json">(.*?)</script>', html, re.S)
    assert m, "search.html must embed a <script id=recipe-index> JSON blob"
    return json.loads(m.group(1))


def test_search_index_extraction_returns_recipes_with_ingredients():
    import search_index

    recipes = search_index.extract_recipes(OEBPS)
    assert len(recipes) > 150
    by_title = {r["title"]: r for r in recipes}
    assert "Apple Cabbage Stew" in by_title
    apple = by_title["Apple Cabbage Stew"]
    assert any("cabbage" in i.lower() for i in apple["ingredients"])
    assert apple["href"].startswith("chapters/")
    assert apple["anchor"]


def test_search_page_has_pantry_ingredient_matching():
    recipes = embedded_index()
    assert len(recipes) > 150
    # Typing "cabbage" as a pantry ingredient should surface cabbage dishes.
    matching = [r["title"] for r in recipes if any("cabbage" in i.lower() for i in r["ingredients"])]
    assert "Apple Cabbage Stew" in matching
    assert "Cabbage Potato Soup" in matching


def test_search_page_contains_query_ui_and_script():
    html = read(DOCS / "search.html")
    assert 'id="pantry-input"' in html
    assert 'id="results"' in html
    assert "addEventListener" in html


def test_every_recipe_has_a_linkable_anchor_in_its_chapter():
    recipes = embedded_index()
    checked = 0
    for r in recipes:
        chapter_file = DOCS / r["href"]
        if not chapter_file.exists():
            continue
        assert f'id="{r["anchor"]}"' in read(chapter_file), f'missing anchor {r["anchor"]} in {r["href"]}'
        checked += 1
    assert checked > 150
