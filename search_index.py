"""Build a searchable index of recipes from the EPUB chapter XHTML.

Used by build_pages.py to generate docs/search.html (pantry-ingredient search)
and by the regression tests.
"""
from __future__ import annotations

import re
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "recipe"


def _clean(text: str) -> str:
    text = TAG_RE.sub("", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    text = text.strip().lstrip("|").strip()
    return re.sub(r"\s+", " ", text)


def _ingredients_from_block(block: str) -> list[str]:
    items: list[str] = []
    # Proper <ul><li> lists (Tears of the Kingdom / Skyrim chapters).
    for li in re.findall(r"<li>(.*?)</li>", block, re.S | re.I):
        cleaned = _clean(li)
        if cleaned:
            items.append(cleaned)
    # Markdown-style "- ingredient" lines inside <p> (early Zelda chapters).
    if not items:
        for line in block.splitlines():
            m = re.match(r"\s*-\s+(.+?)\s*$", line)
            if m:
                cleaned = _clean(m.group(1))
                if cleaned:
                    items.append(cleaned)
    # De-duplicate while preserving order.
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _chapter_title(raw: str, fallback: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S | re.I)
    return _clean(m.group(1)) if m else fallback


def extract_recipes(chapters_dir: Path) -> list[dict]:
    """Return one dict per recipe page across all chapter XHTML files."""
    chapters_dir = Path(chapters_dir)
    recipes: list[dict] = []
    for path in sorted(chapters_dir.glob("chapter*.xhtml")):
        m = re.search(r"chapter(\d+)\.xhtml$", path.name)
        if not m:
            continue
        num = int(m.group(1))
        raw = path.read_text(encoding="utf-8")
        chapter_title = _chapter_title(raw, f"Chapter {num}")
        href = f"chapters/chapter{num:02d}.html"
        # Split into recipe blocks at each <h3> heading.
        parts = re.split(r"(<h3[^>]*>.*?</h3>)", raw, flags=re.S | re.I)
        for i, part in enumerate(parts):
            hm = re.match(r"<h3[^>]*>(.*?)</h3>", part, re.S | re.I)
            if not hm:
                continue
            title = _clean(hm.group(1))
            if not title:
                continue
            block = parts[i + 1] if i + 1 < len(parts) else ""
            block = block.split("<h3", 1)[0]
            recipes.append(
                {
                    "title": title,
                    "anchor": slugify(title),
                    "href": href,
                    "chapter": chapter_title,
                    "chapter_number": num,
                    "ingredients": _ingredients_from_block(block),
                }
            )
    return recipes


if __name__ == "__main__":
    import json
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("book/epub_build/OEBPS")
    data = extract_recipes(target)
    print(f"{len(data)} recipes indexed")
    print(json.dumps(data[:3], indent=2))
