import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TAGS = {"vegetarian", "vegan", "dairy-free", "gluten-free", "quick", "easy"}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def model() -> dict:
    return json.loads(read("data/recipes.json"))


def test_chapters_are_thematic_and_reader_facing():
    m = model()
    titles = [c["title"] for c in m["chapters"]]
    assert len(titles) == 8
    assert not any("Draft" in t for t in titles), f"dev-artifact chapter names remain: {titles}"
    assert titles[0].startswith("Chapter I — Stable Comforts")
    assert titles[-1].startswith("Chapter VIII — Skyrim")
    assert sum(len(c["recipes"]) for c in m["chapters"]) == 211


def test_every_recipe_is_complete():
    for c in model()["chapters"]:
        for r in c["recipes"]:
            for field in ("id", "title", "ingredients", "method", "servings", "time", "difficulty", "tags"):
                assert r.get(field), f"{r.get('title')} missing {field}"
            assert r["ingredients"] and r["method"]
            assert set(r["tags"]) - {c["slug"]} <= ALLOWED_TAGS


def test_sitemap_lists_every_page():
    sitemap = read("docs/sitemap.xml")
    for n in range(1, 15):
        assert f"chapter{n:02d}.html" in sitemap
    assert "search.html" in sitemap
    assert "Sitemap:" in read("docs/robots.txt")


def test_legal_page_and_open_graph_present():
    legal = read("docs/chapters/chapter14.html")
    assert "not affiliated" in legal.lower()
    assert "Nintendo" in legal
    index = read("docs/index.html")
    assert 'property="og:title"' in index and 'property="og:description"' in index


def test_epub_is_valid_and_ordered():
    epub = ROOT / "book" / "The_Wild_Table.epub"
    assert epub.exists()
    with zipfile.ZipFile(epub) as zf:
        assert zf.testzip() is None
        assert zf.namelist()[0] == "mimetype"
        assert zf.read("mimetype") == b"application/epub+zip"
        names = zf.namelist()
        assert "OEBPS/chapter09.xhtml" in names and "OEBPS/chapter14.xhtml" in names


def test_print_edition_exists():
    html = read("book/The_Wild_Table.html")
    assert "Print / Save as PDF" in html and "@media print" in html


def test_zelda_recipes_use_ingame_flavor_text():
    m = model()
    zelda = [r for c in m["chapters"] if c["slug"] != "skyrim" for r in c["recipes"]]
    assert len(zelda) == 160
    assert all(r["note"] for r in zelda), "every BotW/TotK recipe needs flavor text"
    apple = next(r for r in zelda if r["title"] == "Apple Pie")
    assert "match made in heaven" in apple["note"]
    # the old generic filler must be gone everywhere
    assert not any("better than it needs to be" in r["note"]
                   for c in m["chapters"] for r in c["recipes"])
