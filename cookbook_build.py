"""Unified cookbook builder.

Generates every artifact from the canonical model (cookbook_model.build_model):
  - manuscript/The_Wild_Table_v0.6.md
  - book/epub_build/OEBPS/* + book/The_Wild_Table.epub
  - book/The_Wild_Table.html (single-file print edition)
  - docs/ static GitHub Pages site (hero index, chapters, filterable search,
    sitemap.xml, robots.txt, legal page, category icons, Open Graph tags)
"""
from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import cookbook_model as cm

ROOT = Path(__file__).resolve().parent
OEBPS = ROOT / "book" / "epub_build" / "OEBPS"
DOCS = ROOT / "docs"
SITE = "https://servbt.github.io/botw-cookbook"
SUBTITLE = "An Unofficial Real-World Cookbook Inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim"

ICONS = {
    "front": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5a2 2 0 0 1 2-2h11v18H6a2 2 0 0 1-2-2z"/><path d="M17 3v18"/><path d="M7 7h7M7 11h7"/></svg>',
    "stable-comforts": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 9h16v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z"/><path d="M9 9c0-2 1-3 3-3s3 1 3 3"/><path d="M8 5c0-1 .5-1.5 1-2M12 4c0-1 .5-1.5 1-2M16 5c0-1 .5-1.5 1-2"/></svg>',
    "road-food": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20 20 4"/><rect x="6" y="14" width="4" height="4"/><rect x="10" y="10" width="4" height="4"/><rect x="14" y="6" width="4" height="4"/></svg>',
    "rice-curry-bowls": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 11h16a8 8 0 0 1-8 8 8 8 0 0 1-8-8z"/><path d="M3 11h18"/><circle cx="9" cy="8" r=".8"/><circle cx="12" cy="7" r=".8"/><circle cx="15" cy="8" r=".8"/></svg>',
    "from-the-coasts": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 12c4 3 10 3 14 0 3-2 3-6 0-6-2 0-3 1-3 3"/><circle cx="12" cy="12" r="1.4"/><path d="M12 5v-2"/></svg>',
    "sweets": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 12h14v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path d="M5 12c1.5-2 4-3 7-3s5.5 1 7 3"/><path d="M12 9V5M12 5c1-1 2-1 2-1"/><path d="M8 16h8"/></svg>',
    "elixirs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 3h4v4l3 5v7a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1v-7l3-5z"/><path d="M9 14h6"/></svg>',
    "totk": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3c5 4 8 6 8 10a8 8 0 0 1-16 0c0-4 3-6 8-10z"/><path d="M12 9v6M9 12h6"/></svg>',
    "skyrim": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 3h8l3 4-1 12H7L6 7z"/><path d="M9 7h4M9 11h4M9 15h3"/></svg>',
    "appendix": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8l1.5 1.5L12 7M8 14l1.5 1.5L12 13"/><path d="M14 8h3M14 14h3"/></svg>',
    "legal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
}

FRONT_MATTER = """
<h2>How to use this book</h2>
<p>Every recipe here begins with the in-game dish that inspired it and the real-world version you can
actually cook. Amounts are written for a home kitchen: taste as you go and adjust. Salt, pepper, and
fat (butter or oil) are assumed; where a recipe lists them, they are worth getting right.</p>
<p>Difficulty runs <strong>Easy</strong>, <strong>Medium</strong>, or <strong>Hard</strong>. Times are honest but approximate, and
soups and stews are always better the next day.</p>

<h2>Pantry translation guide</h2>
<ul>
<li><strong>Tabantha Wheat:</strong> all-purpose flour, bread flour, pie crust, pasta, or cooked wheat berries</li>
<li><strong>Hylian Rice:</strong> short-grain rice, sushi rice, arborio, jasmine, or calrose</li>
<li><strong>Goat Butter:</strong> butter; goat butter if available</li>
<li><strong>Fresh Milk:</strong> whole milk; oat milk for dairy-free versions</li>
<li><strong>Rock Salt / Salt Pile:</strong> kosher salt or flaky sea salt</li>
<li><strong>Goron Spice:</strong> Japanese curry powder, garam masala, smoked paprika, chili, or a house curry blend</li>
<li><strong>Monster Extract / Dark Clump:</strong> berry reduction, black garlic molasses, squid ink, balsamic glaze, or dark spice syrup</li>
<li><strong>Hearty ingredients:</strong> avocado, egg, salmon, beans, mushrooms, or root vegetables</li>
<li><strong>Elixir critters / monster parts:</strong> herbs, teas, spices, fruit, caffeine-free tonics, or sparkling drinks</li>
</ul>

<h2>Substitutions for the game's rarer items</h2>
<ul>
<li><strong>Horker meat:</strong> pork shoulder, bacon, or smoked ham</li>
<li><strong>Mammoth snout:</strong> beef short rib, oxtail, or brisket</li>
<li><strong>Horse meat:</strong> lean beef or venison</li>
<li><strong>Leg of goat:</strong> goat, lamb, or bone-in pork</li>
<li><strong>Pheasant:</strong> chicken thigh or turkey cutlet</li>
<li><strong>Hateno cheese:</strong> aged cheddar, gouda, or gruyère</li>
<li><strong>Moon sugar:</strong> brown sugar or honey</li>
</ul>

<h2>Conversions</h2>
<ul>
<li>1 cup flour ≈ 120 g · 1 cup sugar ≈ 200 g · 1 cup rice ≈ 190 g</li>
<li>1 tbsp ≈ 15 ml · 1 tsp ≈ 5 ml · 1 stick butter ≈ 113 g</li>
<li>350°F = 175°C · 375°F = 190°C · 400°F = 200°C · 425°F = 220°C</li>
</ul>

<h2>Dietary tags</h2>
<p>Recipe cards on the website carry optional tags — <em>vegetarian</em>, <em>vegan</em>, <em>dairy-free</em>,
<em>gluten-free</em>, <em>quick</em> — to help you cook from what you already have. Treat them as a guide, not a
guarantee: always check your own labels.</p>

<h2>A note on this being a fan work</h2>
<p>This is an original, unofficial fan cookbook. Each dish card quotes the short in-game flavor text for
that meal (from <em>Breath of the Wild</em> / <em>Tears of the Kingdom</em>); everything else — recipes, prose, and
illustrations — is original real-world adaptation. It contains no official art, logos, or screenshots, and is
not affiliated with or endorsed by Nintendo or Bethesda. See the <a href="chapter14.html">Legal &amp; Disclaimer</a> page.</p>
""".strip()

LEGAL_BODY = """
<h2>Unofficial fan work</h2>
<p><em>The Wild Table</em> is an independent, unofficial fan project. It is not affiliated with, authorized by,
or endorsed by Nintendo, Bethesda Softworks, ZeniMax, or any of their subsidiaries or affiliates.</p>
<p>The Legend of Zelda, Breath of the Wild, Tears of the Kingdom, The Elder Scrolls, and Skyrim are trademarks
of their respective owners. All names are used descriptively to explain what inspired each recipe.</p>
<h2>Content</h2>
<p>All recipes, real-world instructions, prose, and illustrations in this book are original adaptations created
for this project. Each dish card also quotes the short in-game flavor text for that meal, which remains the
property of its respective rights holders and is included descriptively. No official artwork, logos,
screenshots, or other copied in-game text are included.</p>
<h2>Use</h2>
<p>Cook everything at your own risk and use normal kitchen safety. Adapt recipes to your own dietary needs.
AI-generated or self-authored illustrations and icons are original works.</p>
""".strip()


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def all_recipes(model):
    for c in model["chapters"]:
        for r in c["recipes"]:
            yield c, r


# ------------------------------------------------------------------ recipe html

def recipe_html(r: dict) -> str:
    meta = f"<strong>Inspired by:</strong> {esc(r['inspired_by'])}<br/>"
    if r.get("real_version"):
        meta += f"<strong>Real-world version:</strong> {esc(r['real_version'])}<br/>"
    dialine = []
    if r.get("servings"):
        dialine.append(f"<strong>Serves:</strong> {esc(r['servings'])}")
    if r.get("time"):
        dialine.append(f"<strong>Time:</strong> {esc(r['time'])}")
    if r.get("difficulty"):
        dialine.append(f"<strong>Difficulty:</strong> {esc(r['difficulty'])}")
    meta += f'<span class="dialine">{" · ".join(dialine)}</span>'
    ings = "".join(f"<li>{esc(i)}</li>" for i in r["ingredients"])
    steps = "".join(f"<li>{esc(s)}</li>" for s in r["method"])
    note = f'<p class="serving-note"><em>{esc(r["note"])}</em></p>' if r.get("note") else ""
    return (
        f'<article class="recipe" id="{esc(r["id"])}">'
        f'<h3>{esc(r["title"])}</h3>'
        f'<p class="recipe-meta">{meta}</p>'
        f'<p class="label">Ingredients</p><ul>{ings}</ul>'
        f'<p class="label">Method</p><ol>{steps}</ol>'
        f'{note}</article>'
    )


# ------------------------------------------------------------------ manuscript

def build_manuscript(model, appendices):
    lines = [
        "# The Wild Table",
        f"## {SUBTITLE}",
        "",
        f"**Draft:** v0.6  ",
        f"**Status:** {sum(len(c['recipes']) for c in model['chapters'])} recipes across "
        f"{len(model['chapters'])} reader-facing chapters, reorganised thematically from the "
        f"Breath of the Wild, Tears of the Kingdom, and Skyrim sets.",
        "**Important:** original fan work. No Nintendo or Bethesda art, logos, screenshots, or copied text.",
        "",
        "---",
        "",
        "## How to Use This Book",
        "",
        "Every recipe gives the in-game dish that inspired it and a real-world version you can actually cook.",
        "Difficulty is Easy / Medium / Hard; times are approximate. Salt, pepper, and fat are assumed.",
        "",
        "## Pantry Translation Guide",
        "",
        "- **Tabantha Wheat:** all-purpose flour, bread flour, pie crust, pasta, or cooked wheat berries",
        "- **Hylian Rice:** short-grain rice, sushi rice, arborio, jasmine, or calrose",
        "- **Goat Butter:** butter; goat butter if available",
        "- **Fresh Milk:** whole milk; oat milk for dairy-free versions",
        "- **Rock Salt / Salt Pile:** kosher salt or flaky sea salt",
        "- **Goron Spice:** Japanese curry powder, garam masala, smoked paprika, chili, or a house curry blend",
        "- **Monster Extract / Dark Clump:** berry reduction, black garlic molasses, squid ink, balsamic glaze, or dark spice syrup",
        "",
        "## Conversions",
        "",
        "- 1 cup flour ≈ 120 g · 1 cup sugar ≈ 200 g · 1 cup rice ≈ 190 g",
        "- 1 tbsp ≈ 15 ml · 1 tsp ≈ 5 ml · 1 stick butter ≈ 113 g",
        "- 350°F = 175°C · 375°F = 190°C · 400°F = 200°C · 425°F = 220°C",
        "",
        "---",
        "",
    ]
    for ci, c in enumerate(model["chapters"], 1):
        lines.append(f"# {c['title']}")
        lines.append("")
        lines.append(f"_{c['blurb']}_")
        lines.append("")
        for r in c["recipes"]:
            lines.append(f"### {r['title']}")
            lines.append(f"**Inspired by:** {r['inspired_by']}  ")
            if r.get("real_version"):
                lines.append(f"**Real-world version:** {r['real_version']}  ")
            lines.append(f"**Serves:** {r['servings']} | **Time:** {r['time']} | **Difficulty:** {r['difficulty']}  ")
            lines.append(f"**Tags:** {', '.join(r['tags'])}")
            lines.append("")
            lines.append("**Ingredients**")
            lines += [f"- {i}" for i in r["ingredients"]]
            lines.append("")
            lines.append("**Method**")
            lines += [f"{n}. {s}" for n, s in enumerate(r["method"], 1)]
            if r.get("note"):
                lines.append("")
                lines.append(f"**Serving note:** {r['note']}")
            lines.append("")
            lines.append("---")
            lines.append("")
    for a in appendices:
        lines.append(f"# {a['title']}")
        lines.append("")
        for li in re.findall(r"<li>(.*?)</li>", a["body"], re.S):
            text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", li, flags=re.S)
            text = re.sub(r"<[^>]+>", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                lines.append(f"- {text}")
        lines.append("")
    (ROOT / "manuscript" / "The_Wild_Table_v0.6.md").write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ epub

def build_epub(model, appendices):
    for old in OEBPS.glob("chapter*.xhtml"):
        old.unlink()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest, spine, nav_items = [], [], []

    def emit(num, title, body, icon_slug):
        item = f"chapter{num:02d}"
        (OEBPS / f"{item}.xhtml").write_text(
            '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" lang="en"><head><title>{esc(title)}</title>'
            '<link rel="stylesheet" type="text/css" href="styles/style.css"/></head>'
            f'<body><main class="book"><h1>{esc(title)}</h1>\n{body}\n</main></body></html>',
            encoding="utf-8")
        manifest.append(f'<item id="{item}" href="{item}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{item}"/>')
        rel = f"{item}.xhtml"
        nav_items.append(f'<li><a href="{rel}">{esc(title)}</a></li>')

    emit(1, "Front Matter — How to Use This Book", FRONT_MATTER, "front")
    for ci, c in enumerate(model["chapters"], 2):
        body = f'<p class="blurb">{esc(c["blurb"])}</p>\n' + "\n".join(recipe_html(r) for r in c["recipes"])
        emit(ci, c["title"], body, c["slug"])
    for ai, a in enumerate(appendices, 2 + len(model["chapters"])):
        emit(ai, a["title"], a["body"], "appendix")
    emit(2 + len(model["chapters"]) + len(appendices), "Legal & Disclaimer", LEGAL_BODY, "legal")

    (OEBPS / "nav.xhtml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">'
        '<head><title>Contents</title><link rel="stylesheet" type="text/css" href="styles/style.css"/></head>'
        '<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>' + "\n".join(nav_items) + '</ol></nav></body></html>',
        encoding="utf-8")

    (OEBPS / "content.opf").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">\n'
        '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        '    <dc:identifier id="bookid">urn:uuid:e90eb269-c672-43b6-88e4-6f9d04182614</dc:identifier>\n'
        '    <dc:title>The Wild Table</dc:title>\n'
        '    <dc:creator>Arian Rezvani with Hermes Agent</dc:creator>\n'
        '    <dc:language>en</dc:language>\n'
        '    <dc:description>An unofficial real-world cookbook inspired by Breath of the Wild, '
        'Tears of the Kingdom, and Skyrim cooking, with original recipes.</dc:description>\n'
        f'    <meta property="dcterms:modified">{now}</meta>\n'
        '  </metadata>\n  <manifest>\n'
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
        '    <item id="css" href="styles/style.css" media-type="text/css"/>\n'
        + "\n    ".join(manifest) +
        '\n  </manifest>\n  <spine>\n    ' + "\n    ".join(spine) +
        '\n  </spine>\n</package>', encoding="utf-8")

    epub = ROOT / "book" / "The_Wild_Table.epub"
    if epub.exists():
        epub.unlink()
    with zipfile.ZipFile(epub, "w") as zf:
        zf.write(ROOT / "book" / "epub_build" / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted((ROOT / "book" / "epub_build").rglob("*")):
            if p.is_file() and p.name != "mimetype":
                zf.write(p, p.relative_to(ROOT / "book" / "epub_build").as_posix(), compress_type=zipfile.ZIP_DEFLATED)


# ------------------------------------------------------------------ print edition

def build_print_edition(model, appendices):
    parts = [f'<h1 class="cover">{esc("The Wild Table")}</h1><p class="cover-sub">{esc(SUBTITLE)}</p>',
             '<p class="cover-sub">Unofficial fan work — original recipes, no official art.</p>',
             '<button class="print-btn" onclick="window.print()">Print / Save as PDF</button>',
             FRONT_MATTER]
    for c in model["chapters"]:
        parts.append(f'<h1>{esc(c["title"])}</h1><p class="blurb">{esc(c["blurb"])}</p>')
        parts += [recipe_html(r) for r in c["recipes"]]
    for a in appendices:
        parts.append(f'<h1>{esc(a["title"])}</h1>{a["body"]}')
    parts.append(f'<h1>Legal &amp; Disclaimer</h1>{LEGAL_BODY}')
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>{esc("The Wild Table")}</title><style>{PRINT_CSS}</style></head>'
           '<body><main class="book">' + "\n".join(parts) + '</main></body></html>')
    (ROOT / "book" / "The_Wild_Table.html").write_text(doc, encoding="utf-8")


PRINT_CSS = """
:root{--paper:#fffdf7;--ink:#24170f;--muted:#6f5946;--accent:#b56a1d;--line:#e2c9a6;}
*{box-sizing:border-box;} body{margin:0;background:#fffaf0;color:var(--ink);font-family:Georgia,'Times New Roman',serif;line-height:1.55;}
.book{max-width:820px;margin:0 auto;padding:40px 34px 90px;background:var(--paper);}
h1{font-size:2.3rem;color:#5a2f12;border-bottom:3px solid var(--accent);padding-bottom:.3rem;margin-top:2.4rem;page-break-before:always;}
h1.cover{border:0;text-align:center;font-size:3.2rem;page-break-before:auto;margin-top:16vh;}
.cover-sub{text-align:center;color:var(--muted);font-style:italic;}
h3{font-size:1.3rem;color:#3b2415;margin-top:1.8rem;border-top:1px solid var(--line);padding-top:1rem;}
.recipe-meta{color:var(--muted);} .dialine{color:var(--muted);}
.label{font-weight:bold;margin-bottom:.2rem;} ul,ol{padding-left:1.3rem;}
.serving-note{color:var(--muted);font-style:italic;border-left:3px solid var(--accent);padding-left:.8rem;}
.blurb{color:var(--muted);font-style:italic;} .print-btn{display:block;margin:1rem auto;padding:.6rem 1.2rem;font:inherit;border:2px solid var(--accent);border-radius:10px;background:#fff;cursor:pointer;}
a{color:#7a4218;}
@media print{body{background:#fff;} .book{padding:0;max-width:none;} .print-btn{display:none;} h1{page-break-before:always;} h3{page-break-after:avoid;} .recipe{page-break-inside:avoid;}}
"""
