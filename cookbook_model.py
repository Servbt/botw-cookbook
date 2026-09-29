"""Canonical cookbook model.

Single source of truth: parse the manuscript into structured recipes, classify
them into reader-facing thematic chapters, normalise metadata, add dietary tags
and voice notes, then serialise to data/recipes.json for the builders.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript" / "The_Wild_Table_v0.5.md"
MODEL_JSON = ROOT / "data" / "recipes.json"

# Reader-facing chapters in publication order.
CHAPTERS = [
    ("stable-comforts", "Chapter I — Stable Comforts", "Soups, stews, and warm bowls for a cold ride home."),
    ("road-food", "Chapter II — Road Food: Skewers, Roasts & Grills", "Skewers, roasts, and glazed things cooked over an open fire."),
    ("rice-curry-bowls", "Chapter III — Rice, Curry & Village Bowls", "Rice, curry, pilaf, risotto, and hearty bowls."),
    ("from-the-coasts", "Chapter IV — From the Coasts: Seafood", "Fish, crab, clam, and everything from the water."),
    ("sweets", "Chapter V — Sweets, Cakes & Crepes", "Cakes, pies, puddings, crepes, and fruit desserts."),
    ("elixirs", "Chapter VI — Elixirs & Tonics", "Elixirs reborn as real drinks and mocktails."),
    ("totk", "Chapter VII — Tears of the Kingdom Additions", "Non-duplicate Tears of the Kingdom dishes."),
    ("skyrim", "Chapter VIII — Skyrim: A Nord's Table", "Hearty Skyrim cooking, done properly."),
]
CHAPTER_BY_SLUG = {slug: (title, blurb) for slug, title, blurb in CHAPTERS}

# Existing manuscript chapter headings -> nothing here; classification is per recipe.

DESSERT_WORDS = ["cake", "pudding", "tart", "crepe", "candy", "fruitcake", "nutcake",
                 "cheesecake", "honeyed fruit", "honeyed apple", "fried bananas",
                 "wildberry", "simmered fruit", "steamed fruit", "fruit pie", "fruitcake"]
DESSERT_PIE = ("apple pie", "fruit pie", "pumpkin pie")
RICE_WORDS = ["rice", "curry", "pilaf", "risotto", "bowl", "porridge"]
SEA_WORDS = ["seafood", "fish", "salmon", "crab", "clam", "porgy", "paella", "snail",
             "meuni", "risotto of the sea", "seafood"]
ROAD_WORDS = ["skewer", "roast", "grill", "fried", "glazed", "steak", "drumstick", "thigh", "chop"]

MEAT_WORDS = ["meat", "beef", "chicken", "pork", "poultry", "steak", "sausage", "venison", "lamb",
              "drumstick", "thigh", "bacon", "ham", "horker", "mammoth", "boar", "bird", "goat"]
FISH_WORDS = ["fish", "seafood", "salmon", "crab", "clam", "porgy", "shrimp", "mussel", "trout",
              "bass", "carp", "catfish", "cod", "snail", "mudcrab", "anthias", "spiderfish", "goldfish"]
DAIRY_WORDS = ["milk", "butter", "cheese", "cream", "yogurt"]
GLUTEN_WORDS = ["flour", "wheat", "bread", "crust", "pasta", "crepe", "pie", "pastry", "cracker", "biscuit"]
EGG_WORDS = ["egg"]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------------------------------------------------------------- parsing

def _field(block: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}:?\*\*\s*(.+)", block)
    return m.group(1).strip().rstrip("  ") if m else ""


def parse_manuscript(path: Path = MANUSCRIPT) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^#{1,3} .+$", text, re.M))
    recipes: list[dict] = []
    current_chapter = ""
    for i, m in enumerate(headings):
        heading = m.group(0)
        if heading.startswith("# "):
            current_chapter = heading[2:].strip()
            continue
        if not heading.startswith("### "):
            continue
        title = heading[4:].strip()
        start = m.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        block = text[start:end]
        block = block.split("\n# ", 1)[0]

        inspired = _field(block, "Inspired by").lstrip("| ").strip()
        real = _field(block, "Real-world version").lstrip("| ").strip()

        servings = ""
        mt = re.search(r"Serves:?\**\s*([^|\n]+)", block) or re.search(r"Makes:?\**\s*([^|\n]+)", block)
        if mt:
            servings = mt.group(1).strip().rstrip("*").strip()
        mtime = re.search(r"Time:?\**\s*([^|\n]+)", block)
        difficulty = re.search(r"Difficulty:?\**\s*([A-Za-z]+)", block)

        ing_match = re.search(r"\*\*Ingredients\*\*(.*?)\*\*Method\*\*", block, re.S)
        ingredients = []
        if ing_match:
            for line in ing_match.group(1).splitlines():
                lm = re.match(r"\s*[-*]\s+(.+)", line)
                if lm:
                    ingredients.append(lm.group(1).strip())

        meth_match = re.search(r"\*\*Method\*\*(.*)$", block, re.S)
        method = []
        if meth_match:
            for line in meth_match.group(1).splitlines():
                lm = re.match(r"\s*\d+\.\s+(.+)", line)
                if lm:
                    method.append(lm.group(1).strip())

        note = ""
        nm = re.search(r"\*\*(?:Camp note|Serving note|Note):\*\*\s*(.+)", block)
        if nm:
            note = nm.group(1).strip()

        recipes.append({
            "id": slugify(title),
            "title": title,
            "source_chapter": current_chapter,
            "inspired_by": inspired,
            "real_version": real,
            "servings": re.sub(r"\s+", " ", servings),
            "time": mtime.group(1).strip().rstrip("*").strip() if mtime else "",
            "difficulty": difficulty.group(1).strip() if difficulty else "Easy",
            "ingredients": ingredients,
            "method": method,
            "note": note,
        })
    return recipes


# ---------------------------------------------------------------- classification

def classify(recipe: dict) -> str:
    src = recipe.get("source_chapter", "")
    if "Tears of the Kingdom" in src:
        return "totk"
    if "Skyrim" in src:
        return "skyrim"
    if "elixir" in recipe["title"].lower() or "tonic" in recipe["title"].lower():
        return "elixirs"
    low = recipe["title"].lower()
    if low in DESSERT_PIE or any(w in low for w in DESSERT_WORDS):
        return "sweets"
    if any(w in low for w in RICE_WORDS):
        return "rice-curry-bowls"
    if any(w in low for w in SEA_WORDS):
        return "from-the-coasts"
    if any(w in low for w in ROAD_WORDS):
        return "road-food"
    return "stable-comforts"


def dietary_tags(recipe: dict) -> list[str]:
    blob = " ".join(recipe["ingredients"] + [recipe["title"]]).lower()
    tags = []
    has_meat = any(w in blob for w in MEAT_WORDS)
    has_fish = any(w in blob for w in FISH_WORDS)
    if not has_meat and not has_fish:
        tags.append("vegetarian")
        if not any(w in blob for w in DAIRY_WORDS + EGG_WORDS):
            tags.append("vegan")
    if not any(w in blob for w in DAIRY_WORDS):
        tags.append("dairy-free")
    if not any(w in blob for w in GLUTEN_WORDS):
        tags.append("gluten-free")
    if recipe["difficulty"].lower() == "easy":
        tags.append("easy")
    return tags


def _minutes(time_text: str) -> int:
    total = 0
    for value, unit in re.findall(r"(\d+)\s*(hr|hour|min)", time_text.lower()):
        total += int(value) * (60 if unit.startswith(("hr", "hour")) else 1)
    return total


FALLBACK_NOTES = [
    "Simple, honest, and better than it needs to be.",
    "A good one to know by heart.",
    "Worth making once and then again by memory.",
    "Rustic and unfussy — the way camp food should be.",
    "Tastes like a longer trip than it took.",
    "Keep this one in the back pocket.",
]


def build_model() -> dict:
    import cookbook_overlays as ov

    recipes = parse_manuscript()
    chapters = {slug: {"slug": slug, "title": title, "blurb": blurb, "recipes": []}
                for slug, title, blurb in CHAPTERS}
    for r in recipes:
        slug = classify(r)
        r["chapter"] = slug
        if slug == "skyrim" and r["title"] in ov.SKYRIM_METHODS:
            r["method"] = ov.SKYRIM_METHODS[r["title"]]
        if slug == "skyrim":
            r["note"] = ov.SKYRIM_NOTES.get(r["title"], "")
        elif not r["note"]:
            r["note"] = ov.ZELDA_NOTES.get(r["title"], "")
        if not r["note"]:
            r["note"] = FALLBACK_NOTES[len(r["title"]) % len(FALLBACK_NOTES)]
        r["tags"] = [slug] + dietary_tags(r)
        if _minutes(r["time"]) and _minutes(r["time"]) <= 30:
            r["tags"].append("quick")
        chapters[slug]["recipes"].append(r)
    for c in chapters.values():
        c["recipes"].sort(key=lambda x: x["title"].lower())
    return {"chapters": [chapters[s] for s, _, _ in CHAPTERS]}

