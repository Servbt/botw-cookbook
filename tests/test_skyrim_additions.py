from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SKYRIM_RECIPES = [
    "Apple Cabbage Stew",
    "Beef Stew",
    "Elsweyr Fondue",
    "Horker Stew",
    "Mammoth Steak",
    "Salmon Steak",
    "Steamed Mudcrab Legs",
    "Venison Stew",
]

EXPECTED_SKIPPED_VARIANTS = [
    "Hot Beef Stew",
    "Hot Vegetable Soup",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_skyrim_cooking_recipes_exist_as_their_own_chapter_in_manuscript():
    manuscript = read("manuscript/The_Wild_Table_v0.5.md")
    assert "# Chapter VII — Skyrim Cooking Recipes" in manuscript
    skyrim_chapter = manuscript.split("# Chapter VII — Skyrim Cooking Recipes", 1)[1]
    for title in EXPECTED_SKYRIM_RECIPES:
        assert f"### {title}" in skyrim_chapter


def test_skyrim_survival_hot_soup_variants_are_documented_not_repeated():
    manuscript = read("manuscript/The_Wild_Table_v0.5.md")
    skyrim_chapter = manuscript.split("# Chapter VII — Skyrim Cooking Recipes", 1)[1]
    assert "Survival Mode hot soups" in skyrim_chapter
    for title in EXPECTED_SKIPPED_VARIANTS:
        assert f"### {title}" not in skyrim_chapter


def test_epub_and_static_site_include_skyrim_chapter():
    nav = read("book/epub_build/OEBPS/nav.xhtml")
    index = read("docs/index.html")
    chapter = read("docs/chapters/chapter12.html")
    assert "Chapter VII — Skyrim Cooking Recipes" in nav
    assert "Chapter VII — Skyrim Cooking Recipes" in index
    for title in EXPECTED_SKYRIM_RECIPES:
        assert title in chapter
