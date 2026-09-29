from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TOTK_ADDITIONS = [
    "Steamed Tomatoes", "Cooked Stambulb", "Buttered Stambulb", "Fragrant Seafood Stew",
    "Deep-Fried Drumstick", "Simmered Tomato", "Fruity Tomato Stew", "Tomato Mushroom Stew",
    "Tomato Seafood Soup", "Cheesy Curry", "Cheesy Risotto", "Crunchy Fried Rice",
    "Cheesy Meat Bowl", "Veggie Porridge", "Melty Cheesy Bread", "Hylian Tomato Pizza",
    "Cheesy Tomato", "Cheesy Baked Fish", "Cheesy Omelet", "Cheesecake", "Noble Pursuit",
    "Dark Stew", "Dark Soup", "Dark Curry", "Dark Rice Ball", "Dark Cake",
    "Bright Elixir", "Sticky Elixir",
]

EXCLUDED_AS_DUPLICATES = ["Honey Candy", "Honey Crepe", "Milk", "Snail Chowder"]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_totk_additions_are_own_chapter_in_manuscript():
    manuscript = read("manuscript/The_Wild_Table_v0.6.md")
    assert "# Chapter VII — Tears of the Kingdom Additions" in manuscript
    chapter = manuscript.split("# Chapter VII — Tears of the Kingdom Additions", 1)[1]
    for title in EXPECTED_TOTK_ADDITIONS:
        assert f"### {title}" in chapter


def test_semantic_duplicates_are_not_added_as_totk_pages():
    chapter = read("manuscript/The_Wild_Table_v0.6.md").split(
        "# Chapter VII — Tears of the Kingdom Additions", 1)[1]
    for title in EXCLUDED_AS_DUPLICATES:
        assert f"### {title}" not in chapter


def test_totk_chapter_page_published():
    chapter = read("docs/chapters/chapter08.html")
    assert "Tears of the Kingdom Additions" in chapter
    for title in ["Steamed Tomatoes", "Cheesecake", "Sticky Elixir"]:
        assert title in chapter
