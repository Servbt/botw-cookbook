from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TOTK_ADDITIONS = [
    "Steamed Tomatoes",
    "Cooked Stambulb",
    "Buttered Stambulb",
    "Fragrant Seafood Stew",
    "Deep-Fried Drumstick",
    "Deep-Fried Thigh",
    "Deep-Fried Bird Roast",
    "Simmered Tomato",
    "Fruity Tomato Stew",
    "Tomato Mushroom Stew",
    "Tomato Seafood Soup",
    "Cheesy Curry",
    "Cheesy Risotto",
    "Crunchy Fried Rice",
    "Cheesy Meat Bowl",
    "Prime Cheesy Meat Bowl",
    "Gourmet Cheesy Meat Bowl",
    "Veggie Porridge",
    "Melty Cheesy Bread",
    "Hylian Tomato Pizza",
    "Cheesy Tomato",
    "Cheesy Baked Fish",
    "Cheesy Omelet",
    "Cheesecake",
    "Noble Pursuit",
    "Dark Stew",
    "Dark Soup",
    "Dark Curry",
    "Dark Rice Ball",
    "Dark Cake",
    "Bright Elixir",
    "Sticky Elixir",
]

EXCLUDED_AS_DUPLICATES = [
    "Honey Candy",
    "Honey Crepe",
    "Milk",
    "Snail Chowder",
    "Sauteed Nuts",
    "Herb Saute",
    "Fragrant Mushroom Saute",
    "Seafood Meuniere",
    "Porgy Meuniere",
    "Salmon Meuniere",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_totk_additions_exist_as_their_own_chapter_in_manuscript():
    manuscript = read("manuscript/The_Wild_Table_v0.5.md")
    assert "# Chapter VI — Tears of the Kingdom Additions" in manuscript
    for title in EXPECTED_TOTK_ADDITIONS:
        assert f"### {title}" in manuscript


def test_semantic_duplicates_are_not_added_as_totk_recipe_pages():
    manuscript = read("manuscript/The_Wild_Table_v0.5.md")
    totk_chapter = manuscript.split("# Chapter VI — Tears of the Kingdom Additions", 1)[1]
    for title in EXCLUDED_AS_DUPLICATES:
        assert f"### {title}" not in totk_chapter


def test_epub_and_static_site_include_totk_chapter():
    nav = read("book/epub_build/OEBPS/nav.xhtml")
    index = read("docs/index.html")
    chapter = read("docs/chapters/chapter11.html")
    assert "Chapter VI — Tears of the Kingdom Additions" in nav
    assert "Chapter VI — Tears of the Kingdom Additions" in index
    for title in EXPECTED_TOTK_ADDITIONS:
        assert title in chapter
