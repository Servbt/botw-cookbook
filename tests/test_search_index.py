import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def read(path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def model() -> dict:
    html = read("docs/search.html")
    m = re.search(r'<script id="recipe-index" type="application/json">(.*?)</script>', html, re.S)
    assert m, "search.html must embed a <script id=recipe-index> JSON blob"
    return json.loads(m.group(1).replace("<\\/", "</"))


def flat(m: dict) -> list:
    out = []
    for c in m["chapters"]:
        for r in c["recipes"]:
            out.append(dict(r, chapterTitle=c["title"]))
    return out


def test_embedded_index_has_all_recipes():
    data = flat(model())
    assert len(data) == 211
    by_title = {r["title"]: r for r in data}
    assert "Apple Cabbage Stew" in by_title
    assert any("cabbage" in i.lower() for i in by_title["Apple Cabbage Stew"]["ingredients"])


def test_pantry_matching_surfaces_expected_dishes():
    data = flat(model())
    matching = [r["title"] for r in data if any("cabbage" in i.lower() for i in r["ingredients"])]
    assert "Apple Cabbage Stew" in matching
    assert "Cabbage Potato Soup" in matching


def test_search_page_has_filters_and_query_ui():
    html = read("docs/search.html")
    for token in ['id="pantry-input"', 'id="results"', 'id="category-filters"',
                  'id="tag-filters"', "addEventListener", "activeTag"]:
        assert token in html, f"search.html missing {token}"


def test_every_recipe_has_a_linkable_anchor_in_its_chapter():
    data = flat(model())
    for r in data:
        chapter_file = DOCS / f"chapters/chapter{r['chapterNumber']:02d}.html"
        assert chapter_file.exists(), f"missing chapter file for {r['title']}"
        assert f'id="{r["id"]}"' in chapter_file.read_text(encoding="utf-8")
