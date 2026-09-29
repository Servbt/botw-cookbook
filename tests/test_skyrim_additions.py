import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SKYRIM_RECIPES = ["Apple Cabbage Stew", "Beef Stew", "Elsweyr Fondue",
                           "Horker Stew", "Mammoth Steak", "Salmon Steak",
                           "Steamed Mudcrab Legs", "Venison Stew"]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_skyrim_is_own_chapter_in_manuscript():
    manuscript = read("manuscript/The_Wild_Table_v0.6.md")
    assert "# Chapter VIII — Skyrim: A Nord's Table" in manuscript
    chapter = manuscript.split("# Chapter VIII — Skyrim: A Nord's Table", 1)[1]
    for title in EXPECTED_SKYRIM_RECIPES:
        assert f"### {title}" in chapter


def test_skyrim_chapter_page_published():
    chapter = read("docs/chapters/chapter09.html")
    for title in EXPECTED_SKYRIM_RECIPES:
        assert title in chapter


def test_skyrim_methods_are_bespoke_not_templated():
    model = json.loads(read("data/recipes.json"))
    skyrim = next(c for c in model["chapters"] if c["slug"] == "skyrim")
    assert len(skyrim["recipes"]) == 51
    texts = [re.sub(r"\s+", " ", " ".join(r["method"])).strip() for r in skyrim["recipes"]]
    dupes = [t for t, n in Counter(texts).items() if n > 1]
    assert not dupes, f"{len(dupes)} templated/repeated Skyrim methods remain"
    assert all(r["note"] for r in skyrim["recipes"])
