from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
import json
import re
import shutil
import subprocess
import zipfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OEBPS = ROOT / "book" / "epub_build" / "OEBPS"
SOURCE_URL = "https://en.uesp.net/w/api.php?action=parse&page=Skyrim:Food&prop=wikitext&format=json"
CHAPTER_TITLE = "Chapter VII — Skyrim Cooking Recipes"

SKIP_HOT_NOTE = "Survival Mode hot soups are not repeated as full pages; they are the same base soups with Fire Salts added for warmth."

SUBSTITUTIONS = {
    "Horker Meat": "pork shoulder, bacon, or smoked ham",
    "Mammoth Snout": "beef short rib, oxtail, or brisket",
    "Horse Meat": "lean beef or venison",
    "Leg of Goat": "goat, lamb, or bone-in pork",
    "Pheasant Breast": "pheasant, chicken breast, or turkey cutlet",
    "Venison": "venison, beef, or lamb",
    "Boar Meat": "pork shoulder or wild boar",
    "Nix-Hound Meat": "sausage, pork, or mushroom pieces",
    "Charred Skeever Hide": "charred mushroom, toasted nori, or smoked jerky",
    "Ironwood Fruit": "apple, pear, or quince",
    "Moon Sugar": "brown sugar or honey",
    "Eidar Cheese Wheel": "aged cheddar, gouda, or gruyère",
    "Ale": "amber ale, beer, or nonalcoholic malt drink",
    "Salt Pile": "kosher salt",
    "Sack of Flour": "all-purpose flour",
    "Jug of Milk": "whole milk",
    "Red Apple": "red apple",
    "Ash Yam": "sweet potato or yam",
    "Mudcrab Legs": "crab legs",
}


def clean_markup(text: str) -> str:
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[Skyrim:([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[SR:([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[Skyrim:([^\]]+)\]\]", lambda m: m.group(1).replace("_", " "), text)
    text = re.sub(r"\[\[SR:([^\]]+)\]\]", lambda m: m.group(1).replace("_", " "), text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_wikitext() -> str:
    req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["parse"]["wikitext"]["*"]


def extract_entries(wt: str):
    section = wt.split("==Player-Cooked Food==", 1)[1].split("==={{Anchor|Hot Soups", 1)[0]
    hot_section = wt.split("==={{Anchor|Hot Soups", 1)[1].split("==Other Food==", 1)[0]
    chunks = re.split(r"\n\|-\{\{HE\|", section)[1:]
    entries = []
    seen = set()
    for chunk in chunks:
        raw_title = chunk.split("}}", 1)[0].split("|", 1)[0]
        title = clean_markup(raw_title)
        if title in seen:
            continue
        seen.add(title)
        lines = chunk.splitlines()
        ing_line = ""
        for line in lines:
            if "[[Skyrim:" in line and "<br>" in line and not any(x in line for x in ["File:", "ID|"]):
                ing_line = line.strip("|")
        ingredients = [clean_markup(x) for x in re.split(r"<br\s*/?>", ing_line) if clean_markup(x)]
        entries.append({"title": title, "ingredients": ingredients})
    hot_titles = []
    for m in re.findall(r"\|-\{\{HE\|([^}|]+)", hot_section):
        title = clean_markup(m)
        if title not in hot_titles:
            hot_titles.append(title)
    return entries, hot_titles


def real_ingredient(item: str) -> str:
    item = item.replace(" (item)", "")
    return SUBSTITUTIONS.get(item, item.lower())


def real_version(title: str) -> str:
    if "Fondue" in title:
        return "ale-cheese fondue"
    if "Bisque" in title:
        return "creamy crab bisque"
    if "Chowder" in title:
        return "hearty crab or clam chowder"
    if "Stew" in title:
        return "Nord-style hearth stew"
    if "Soup" in title:
        return "simple tavern soup"
    if "Loaf" in title:
        return "savory meatloaf"
    if "Roast" in title:
        return "salt-roasted game bird or meat"
    if "Steak" in title:
        return "pan-seared steak"
    if "Chop" in title or "Haunch" in title:
        return "seared game cut"
    if "Chicken" in title:
        return "grilled chicken breast"
    if "Mudcrab" in title:
        return "buttered crab legs"
    if title.startswith("Cooked"):
        return "salt-pan cooked fish or meat"
    return "Skyrim-inspired tavern dish"


def pantry_line(ingredients):
    if not ingredients:
        return ["Kosher salt", "Olive oil or butter", "Fresh herbs"]
    out = []
    for ing in ingredients:
        out.append(real_ingredient(ing))
    # make the list kitchen-practical
    extras = []
    joined = " ".join(out).lower()
    if "stew" not in joined and "soup" not in joined and len(out) < 3:
        extras.append("butter or oil")
    if not any("salt" in x for x in out):
        extras.append("kosher salt")
    return [x[0].upper() + x[1:] for x in out + extras]


def method_for(title: str):
    if "Fondue" in title:
        return ["Warm the ale gently in a small pot.", "Add cheese by handfuls, stirring until smooth.", "Sweeten lightly with brown sugar or honey if using.", "Serve hot with bread, apples, or roasted vegetables for dipping."]
    if any(word in title for word in ["Stew", "Soup", "Bisque", "Chowder"]):
        return ["Warm a little butter or oil in a heavy pot.", "Add the sturdy vegetables or aromatics and cook until fragrant.", "Add the meat, fish, crab, or main ingredient with enough stock or water to cover.", "Simmer until tender, then season to taste.", "For creamy soups, stir in milk or butter at the end and keep the heat gentle."]
    if "Loaf" in title:
        return ["Heat oven to 375°F / 190°C.", "Chop the meat finely and mix with salt plus a spoonful of butter or stock.", "Shape into a small loaf on a lined tray.", "Bake until browned and cooked through, then rest before slicing."]
    if any(word in title for word in ["Roast", "Steak", "Chop", "Haunch", "Beef", "Chicken", "Mudcrab", "Salmon"]):
        return ["Pat the main ingredient dry and season with salt.", "Heat butter or oil in a skillet until shimmering.", "Cook until browned on the outside and done in the center.", "Rest briefly, then serve with the pan juices."]
    if title.startswith("Cooked"):
        return ["Pat the fish or meat dry and season with salt.", "Heat a skillet with a small amount of butter or oil.", "Cook until opaque, browned, or cooked through depending on the ingredient.", "Serve simply, tavern-style, with bread or potatoes."]
    return ["Prepare the ingredients into bite-size pieces.", "Cook in a hot pan or pot with butter or oil.", "Season well and serve warm."]


def recipe_md(entry):
    title = entry["title"]
    ingredients = pantry_line(entry["ingredients"])
    lines = [
        f"### {title}",
        f"**Inspired by:** {', '.join(entry['ingredients']) or title}  ",
        f"**Real-world version:** {real_version(title)}  ",
        "**Serves:** 2–4 | **Time:** 20–60 min | **Difficulty:** Easy",
        "",
        "**Ingredients**",
    ]
    lines += [f"- {i}" for i in ingredients]
    lines += ["", "**Method**"]
    lines += [f"{n}. {step}" for n, step in enumerate(method_for(title), 1)]
    lines.append("")
    return "\n".join(lines)


def recipe_xhtml(entry):
    title = entry["title"]
    ingredients = pantry_line(entry["ingredients"])
    html = [
        f"<h3>{escape(title)}</h3>",
        f"<p><strong>Inspired by:</strong> {escape(', '.join(entry['ingredients']) or title)}<br/>",
        f"<strong>Real-world version:</strong> {escape(real_version(title))}<br/>",
        "<strong>Serves: 2–4 | Time: 20–60 min | Difficulty: Easy</strong></p>",
        "<p><strong>Ingredients</strong></p>",
        "<ul>",
    ]
    html += [f"<li>{escape(i)}</li>" for i in ingredients]
    html += ["</ul>", "<p><strong>Method</strong></p>", "<ol>"]
    html += [f"<li>{escape(step)}</li>" for step in method_for(title)]
    html += ["</ol>", "<hr/>"]
    return "\n".join(html)


def add_to_manuscript(entries):
    path = ROOT / "manuscript" / "The_Wild_Table_v0.5.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Breath of the Wild and Tears of the Kingdom", "Breath of the Wild, Tears of the Kingdom, and Skyrim")
    text = re.sub(r"\*\*Status:\*\* working manuscript / \d+ full recipe pages drafted;[^\n]+", f"**Status:** working manuscript / {160 + len(entries)} full recipe pages drafted; Zelda-inspired set plus Skyrim cooking additions adapted", text)
    if f"# {CHAPTER_TITLE}" not in text:
        block = ["", "---", "", f"# {CHAPTER_TITLE}", "", "This chapter adds original real-world adaptations for Skyrim's player-cooked food list. Recipe names and ingredient categories were cross-checked from UESP's Skyrim:Food page via the MediaWiki API.", "", f"**Variant note:** {SKIP_HOT_NOTE}", ""]
        block += [recipe_md(e) + "---\n" for e in entries]
        text += "\n".join(block)
    path.write_text(text, encoding="utf-8")


def write_epub(entries):
    body = ["<?xml version=\"1.0\" encoding=\"utf-8\"?>", "<!DOCTYPE html>", f"<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\"><head><title>{escape(CHAPTER_TITLE)}</title><link rel=\"stylesheet\" type=\"text/css\" href=\"styles/style.css\"/></head><body><main class=\"book\"><h1>{escape(CHAPTER_TITLE)}</h1>", "<p>Original real-world adaptations for Skyrim's player-cooked food list.</p>", f"<p><strong>Variant note:</strong> {escape(SKIP_HOT_NOTE)}</p>"]
    body += [recipe_xhtml(e) for e in entries]
    body.append("</main></body></html>")
    (OEBPS / "chapter12.xhtml").write_text("\n".join(body), encoding="utf-8")

    nav_path = OEBPS / "nav.xhtml"
    nav = nav_path.read_text(encoding="utf-8")
    if "chapter12.xhtml" not in nav:
        nav = nav.replace("<li><a href=\"chapter11.xhtml\">Chapter VI — Tears of the Kingdom Additions</a></li></ol>", f"<li><a href=\"chapter11.xhtml\">Chapter VI — Tears of the Kingdom Additions</a></li>\n<li><a href=\"chapter12.xhtml\">{CHAPTER_TITLE}</a></li></ol>")
    nav_path.write_text(nav, encoding="utf-8")

    opf_path = OEBPS / "content.opf"
    opf = opf_path.read_text(encoding="utf-8")
    opf = re.sub(r"<meta property=\"dcterms:modified\">.*?</meta>", f"<meta property=\"dcterms:modified\">{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>", opf)
    if "chapter12.xhtml" not in opf:
        opf = opf.replace("<item id=\"chap11\" href=\"chapter11.xhtml\" media-type=\"application/xhtml+xml\"/>", "<item id=\"chap11\" href=\"chapter11.xhtml\" media-type=\"application/xhtml+xml\"/>\n<item id=\"chap12\" href=\"chapter12.xhtml\" media-type=\"application/xhtml+xml\"/>")
        opf = opf.replace("<itemref idref=\"chap11\"/>", "<itemref idref=\"chap11\"/>\n<itemref idref=\"chap12\"/>")
    opf_path.write_text(opf, encoding="utf-8")


def update_book_html(entries):
    path = ROOT / "book" / "The_Wild_Table.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Breath of the Wild and Tears of the Kingdom", "Breath of the Wild, Tears of the Kingdom, and Skyrim")
    if CHAPTER_TITLE not in text:
        chapter = [f"<h1>{escape(CHAPTER_TITLE)}</h1>", "<p>Original real-world adaptations for Skyrim's player-cooked food list.</p>", f"<p><strong>Variant note:</strong> {escape(SKIP_HOT_NOTE)}</p>"]
        chapter += [recipe_xhtml(e) for e in entries]
        text = text.replace("</main></body></html>", "\n" + "\n".join(chapter) + "\n</main></body></html>")
    path.write_text(text, encoding="utf-8")


def update_readme(count):
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Breath of the Wild and Tears of the Kingdom", "Breath of the Wild, Tears of the Kingdom, and Skyrim")
    text = text.replace("inspired by Breath of the Wild and Tears of the Kingdom cooking", "inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim cooking")
    if "data/skyrim_uesp_cooking_recipes.json" not in text:
        text = text.replace("- `data/totk_game8_recipes.json` — scraped planning reference for Tears of the Kingdom cooked dishes and elixirs from Game8, used for duplicate screening.", "- `data/totk_game8_recipes.json` — scraped planning reference for Tears of the Kingdom cooked dishes and elixirs from Game8, used for duplicate screening.\n- `data/skyrim_uesp_cooking_recipes.json` — scraped planning reference for Skyrim player-cooked foods from UESP's MediaWiki API.")
    text = re.sub(r"- Drafted \d+ full real-life recipe pages[^\n]+", f"- Drafted {160 + count} full real-life recipe pages, including {count} Skyrim player-cooked food adaptations.", text)
    path.write_text(text, encoding="utf-8")


def update_build_pages():
    path = ROOT / "build_pages.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("range(1, 12)", "range(1, 13)")
    text = text.replace("Breath of the Wild and Tears of the Kingdom", "Breath of the Wild, Tears of the Kingdom, and Skyrim")
    path.write_text(text, encoding="utf-8")


def rebuild_epub():
    epub = ROOT / "book" / "The_Wild_Table.epub"
    build = ROOT / "book" / "epub_build"
    if epub.exists():
        epub.unlink()
    with zipfile.ZipFile(epub, "w") as zf:
        zf.write(build / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(build.rglob("*")):
            if p.is_file() and p.name != "mimetype":
                zf.write(p, p.relative_to(build).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def refresh_archive():
    archive = ROOT / "The_Wild_Table_cookbook_files.zip"
    include = ["README.md", "data", "manuscript", "book", "docs", "build_pages.py", "scripts", "tests"]
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in include:
            path = ROOT / item
            if path.is_file():
                zf.write(path, path.relative_to(ROOT).as_posix())
            elif path.is_dir():
                for f in sorted(path.rglob("*")):
                    if f.is_file() and "__pycache__" not in f.parts:
                        zf.write(f, f.relative_to(ROOT).as_posix())


def main():
    wt = fetch_wikitext()
    entries, hot_titles = extract_entries(wt)
    (ROOT / "data" / "skyrim_uesp_cooking_recipes.json").write_text(json.dumps({"source": "UESP Skyrim:Food MediaWiki API", "source_url": SOURCE_URL, "recipes": entries, "survival_hot_soup_variants_not_repeated": hot_titles}, indent=2), encoding="utf-8")
    add_to_manuscript(entries)
    write_epub(entries)
    update_book_html(entries)
    update_readme(len(entries))
    update_build_pages()
    rebuild_epub()
    subprocess.run(["python3", "build_pages.py"], cwd=ROOT, check=True)
    shutil.copy2(ROOT / "book" / "The_Wild_Table.epub", ROOT / "docs" / "book" / "The_Wild_Table.epub")
    refresh_archive()
    print(f"Added {len(entries)} Skyrim cooking recipe pages; documented {len(hot_titles)} hot soup variants as skipped duplicates.")


if __name__ == "__main__":
    main()
