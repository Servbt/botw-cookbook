
"""Static-site builder for The Wild Table (GitHub Pages).

Consumes the canonical model plus the book builders in cookbook_build.py and
emits docs/: hero index, per-chapter pages, filterable search, sitemap,
robots.txt, and local assets. Run this module directly to build everything.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import cookbook_model as cm
from cookbook_build import (
    DOCS, FRONT_MATTER, ICONS, LEGAL_BODY, ROOT, SITE, SUBTITLE, esc,
    recipe_html, build_manuscript, build_epub, build_print_edition,
)

# ------------------------------------------------------------------ static site

SITE_CSS = """
:root{--bg:#fffaf0;--paper:#fffdf7;--ink:#24170f;--muted:#6f5946;--accent:#b56a1d;--accent-dark:#7a4218;--line:#e2c9a6;--nav:#2f1c10;}
*{box-sizing:border-box;} html{scroll-behavior:smooth;}
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:var(--bg);line-height:1.6;}
a{color:var(--accent-dark);}
.layout{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:100vh;}
.sidebar{position:sticky;top:0;height:100vh;overflow:auto;padding:26px 20px;background:var(--nav);color:#f7ead5;border-right:1px solid rgba(255,255,255,.08);}
.sidebar .brand{display:flex;align-items:center;gap:.5rem;}
.sidebar h1{font-size:1.3rem;margin:0 0 .3rem;line-height:1.15;}
.sidebar .subtitle{margin:0 0 1.2rem;color:#d9c6a9;font-size:.85rem;}
.sidebar nav{display:grid;gap:.3rem;}
.sidebar a{color:#f7ead5;text-decoration:none;display:flex;align-items:center;gap:.55rem;padding:.5rem .6rem;border-radius:10px;border:1px solid transparent;}
.sidebar a svg{width:18px;height:18px;flex:0 0 auto;opacity:.85;}
.sidebar a:hover,.sidebar a.active{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);}
.content{max-width:940px;width:100%;padding:44px 38px 96px;margin:0 auto;background:var(--paper);}
.toplinks{display:flex;gap:1.2rem;flex-wrap:wrap;margin-bottom:1.8rem;color:var(--muted);justify-content:space-between;}
h1{font-size:clamp(2rem,5vw,3.1rem);color:#5a2f12;border-bottom:3px solid var(--accent);padding-bottom:.35rem;margin-top:0;}
h2{font-size:1.5rem;color:var(--accent-dark);margin-top:2rem;}
h3{font-size:1.3rem;color:#3b2415;margin-top:2rem;border-top:1px solid var(--line);padding-top:1.1rem;}
p,li{font-size:1.03rem;} strong{color:#3a2112;}
code{background:#f4e7d2;padding:0 .25em;border-radius:3px;}
hr{border:0;border-top:1px solid var(--line);margin:2rem 0;}
ul,ol{padding-left:1.4rem;}
.chapter-nav{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;padding-top:1.25rem;border-top:1px solid var(--line);}
.chapter-nav a{text-decoration:none;font-weight:bold;}
.notice{background:#f7ead5;border:1px solid var(--line);padding:1rem;border-radius:12px;}
.muted{color:var(--muted);} .blurb{color:var(--muted);font-style:italic;}
.recipe-meta{color:var(--muted);} .dialine{color:var(--muted);}
.label{font-weight:bold;margin-bottom:.2rem;}
.serving-note{color:var(--muted);font-style:italic;border-left:3px solid var(--accent);padding-left:.8rem;}
.chapter-icon{width:52px;height:52px;color:var(--accent);margin-bottom:.4rem;}
.chapter-icon svg{width:100%;height:100%;}
/* hero */
.hero{background:linear-gradient(160deg,#2f1c10,#4a2a14);color:#f7ead5;border-radius:16px;padding:2.2rem 1.8rem;margin-bottom:1.6rem;}
.hero h1{color:#fff;border:0;margin:0 0 .3rem;} .hero p{color:#e5d5bd;margin:.3rem 0 1rem;}
.hero form{display:flex;gap:.6rem;flex-wrap:wrap;}
.hero input{flex:1 1 260px;padding:.8rem 1rem;font-size:1.05rem;font-family:inherit;border:0;border-radius:10px;}
.hero button{padding:.8rem 1.2rem;font:inherit;font-weight:bold;border:0;border-radius:10px;background:var(--accent);color:#24170f;cursor:pointer;}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:1rem;margin:1.2rem 0;}
.card{border:1px solid var(--line);border-radius:12px;padding:1rem;text-decoration:none;color:inherit;display:block;background:#fffdf9;}
.card svg{width:30px;height:30px;color:var(--accent);}
.card h3{border:0;margin:.5rem 0 .2rem;padding:0;font-size:1.05rem;}
.card p{margin:0;color:var(--muted);font-size:.9rem;}
/* search */
.search-box{margin:0 0 1.2rem;} .search-box label{display:block;font-weight:bold;margin-bottom:.4rem;color:#3a2112;}
#pantry-input{width:100%;padding:.8rem 1rem;font-size:1.1rem;font-family:inherit;border:2px solid var(--accent);border-radius:10px;background:var(--paper);color:var(--ink);}
#pantry-input:focus{outline:none;box-shadow:0 0 0 3px rgba(181,106,29,.25);}
.filters{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.2rem;}
.filter{padding:.35rem .7rem;border:1px solid var(--line);border-radius:999px;background:#fffdf9;font:inherit;font-size:.9rem;cursor:pointer;color:var(--muted);}
.filter.active{background:var(--accent);color:#24170f;border-color:var(--accent);font-weight:bold;}
.recipe-hit{border-top:1px solid var(--line);padding-top:1rem;margin-top:1rem;}
.recipe-hit h3{margin-top:0;border-top:0;padding-top:0;}
.recipe-hit h3 a{text-decoration:none;}
.recipe-hit .ingredients{margin:.3rem 0 0;color:var(--muted);}
.tagrow{margin:.3rem 0 0;} .tag{display:inline-block;font-size:.75rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.05rem .5rem;margin-right:.3rem;}
@media (max-width:860px){.layout{display:block;} .sidebar{position:relative;height:auto;} .content{padding:30px 18px 72px;} .toplinks,.chapter-nav{flex-direction:column;}}
@media print{.sidebar,.toplinks,.chapter-nav,.hero,.filters,.search-box{display:none;} .layout{display:block;} .content{padding:0;max-width:none;} body{background:#fff;}}
"""


def _entries(model, appendices):
    entries = [(1, "Front Matter — How to Use This Book", "front")]
    for i, c in enumerate(model["chapters"], 2):
        entries.append((i, c["title"], c["slug"]))
    base = 2 + len(model["chapters"])
    for j, a in enumerate(appendices):
        entries.append((base + j, a["title"], "appendix"))
    entries.append((base + len(appendices), "Legal & Disclaimer", "legal"))
    return entries


def _nav_html(entries, depth, current):
    links = []
    for num, title, icon in entries:
        cls = ' class="active"' if num == current else ""
        links.append(f'<a{cls} href="{depth}chapters/chapter{num:02d}.html">{ICONS[icon]}<span>{esc(title)}</span></a>')
    links.append(f'<a href="{depth}search.html">{ICONS["front"]}<span>Search by ingredient</span></a>')
    return "\n        ".join(links)


def page(title, body, entries, current=None, depth="", og_desc=""):
    nav = _nav_html(entries, depth, current)
    top = (f'<a href="{depth}index.html">Contents</a>'
           f'<a href="{depth}search.html">Search</a>'
           f'<a href="{depth}book/The_Wild_Table.epub">Download EPUB</a>')
    prev_next = ""
    nums = [n for n, _, _ in entries]
    if current in nums:
        i = nums.index(current)
        prev_link = (f'<a href="chapter{nums[i-1]:02d}.html">← {esc(entries[i-1][1])}</a>'
                     if i > 0 else '<a href="../index.html">← Contents</a>')
        next_link = (f'<a href="chapter{nums[i+1]:02d}.html">{esc(entries[i+1][1])} →</a>'
                     if i < len(nums) - 1 else "")
        prev_next = f'<div class="chapter-nav"><div>{prev_link}</div><div>{next_link}</div></div>'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · The Wild Table</title>
  <meta name="description" content="{esc(og_desc or 'An unofficial real-world cookbook inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim.')}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="{esc(title)} · The Wild Table">
  <meta property="og:description" content="{esc(og_desc or 'An unofficial real-world cookbook.')}">
  <meta property="og:url" content="{SITE}/">
  <meta name="twitter:card" content="summary">
  <link rel="stylesheet" href="{depth}styles/site.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">{ICONS["front"]}<h1>The Wild Table</h1></div>
      <p class="subtitle">An unofficial real-world cookbook inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim</p>
      <nav aria-label="Book navigation">
        {nav}
      </nav>
    </aside>
    <main class="content">
      <div class="toplinks">{top}</div>
      {body}
      {prev_next}
    </main>
  </div>
</body>
</html>
'''


def build_site(model, appendices):
    (DOCS / "chapters").mkdir(parents=True, exist_ok=True)
    (DOCS / "styles").mkdir(parents=True, exist_ok=True)
    (DOCS / "book").mkdir(exist_ok=True)
    (DOCS / "styles" / "site.css").write_text(SITE_CSS.strip(), encoding="utf-8")
    shutil.copy2(ROOT / "book" / "The_Wild_Table.epub", DOCS / "book" / "The_Wild_Table.epub")

    entries = _entries(model, appendices)

    # front matter + legal + appendices as chapter pages
    (DOCS / "chapters" / "chapter01.html").write_text(
        page("Front Matter — How to Use This Book", FRONT_MATTER, entries, 1, "../",
             "How to use The Wild Table cookbook: pantry guide, substitutions, conversions, and dietary tags."),
        encoding="utf-8")
    for i, c in enumerate(model["chapters"], 2):
        body = f'<div class="chapter-icon">{ICONS[c["slug"]]}</div><p class="blurb">{esc(c["blurb"])}</p>'
        body += "\n".join(recipe_html(r) for r in c["recipes"])
        (DOCS / "chapters" / f"chapter{i:02d}.html").write_text(
            page(c["title"], body, entries, i, "../", c["blurb"]), encoding="utf-8")
    base = 2 + len(model["chapters"])
    for j, a in enumerate(appendices):
        (DOCS / "chapters" / f"chapter{base+j:02d}.html").write_text(
            page(a["title"], a["body"], entries, base + j, "../", a["title"]), encoding="utf-8")
    legal_num = base + len(appendices)
    (DOCS / "chapters" / f"chapter{legal_num:02d}.html").write_text(
        page("Legal & Disclaimer", LEGAL_BODY, entries, legal_num, "../", "Trademark and content notice."), encoding="utf-8")

    # index with hero + search + chapter cards
    cards = ""
    for num, title, icon in entries:
        if icon in ("front", "legal", "appendix"):
            continue
        c = next(c for c in model["chapters"] if c["title"] == title)
        cards += (f'<a class="card" href="chapters/chapter{num:02d}.html">{ICONS[icon]}'
                  f'<h3>{esc(title)}</h3><p>{esc(c["blurb"])}</p></a>')
    hero = ('<div class="hero"><h1>The Wild Table</h1>'
            f'<p>{esc(SUBTITLE)}</p>'
            '<form action="search.html" method="get"><input name="q" type="search" '
            'placeholder="What\'s in your pantry? e.g. cabbage, egg, mushroom…" aria-label="Search by ingredient">'
            '<button type="submit">Find recipes</button></form></div>')
    index_body = (hero +
                  '<p><a href="chapters/chapter01.html"><strong>How to use this book →</strong></a></p>'
                  '<h2>Chapters</h2><div class="cards">' + cards + '</div>'
                  '<h2>Contents</h2><ol>' +
                  "".join(f'<li><a href="chapters/chapter{n:02d}.html">{esc(t)}</a></li>' for n, t, _ in entries) +
                  '</ol>')
    (DOCS / "index.html").write_text(
        page("The Wild Table", index_body, entries, None, "",
             "A free unofficial real-world cookbook inspired by Breath of the Wild, Tears of the Kingdom, and Skyrim — search by the ingredients you have."),
        encoding="utf-8")

    # search page
    model_json = json.dumps(model, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    search_body = (
        '<h1>Search by ingredient</h1>'
        '<div class="notice">Type an ingredient you have on hand and every matching recipe appears. '
        'Add commas to narrow by several ingredients, then use the filters to refine.</div>'
        '<div class="search-box"><label for="pantry-input">Your pantry ingredients</label>'
        '<input id="pantry-input" type="search" placeholder="cabbage, egg, mushroom…" autocomplete="off"></div>'
        '<div class="filters" id="category-filters"></div>'
        '<div class="filters" id="tag-filters"></div>'
        '<div id="results" aria-live="polite"></div>'
        f'<script id="recipe-index" type="application/json">{model_json}</script>'
        f'<script>{SEARCH_JS}</script>')
    (DOCS / "search.html").write_text(
        page("Search by ingredient", search_body, entries, None, "", "Search The Wild Table by the ingredients in your pantry."),
        encoding="utf-8")

    # sitemap + robots
    urls = [f"{SITE}/", f"{SITE}/search.html"] + [f"{SITE}/chapters/chapter{n:02d}.html" for n, _, _ in entries]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
               "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls) + "\n</urlset>\n")
    (DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


SEARCH_JS = """
(function(){
  var model = JSON.parse(document.getElementById('recipe-index').textContent);
  var data = [];
  model.chapters.forEach(function(c){ c.recipes.forEach(function(r){ r.chapterTitle=c.title; data.push(r); }); });
  var input = document.getElementById('pantry-input');
  var out = document.getElementById('results');
  var catBox = document.getElementById('category-filters');
  var tagBox = document.getElementById('tag-filters');
  var activeCat = 'all';
  var activeTag = 'all';
  var CHAP = {}; model.chapters.forEach(function(c){ CHAP[c.slug]=c.title; });
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function matches(r,t){ if(r.title.toLowerCase().indexOf(t)>-1) return true; return r.ingredients.some(function(i){return i.toLowerCase().indexOf(t)>-1;}); }
  function chip(label,value,box,kind){
    var b=document.createElement('button'); b.className='filter'; b.type='button'; b.textContent=label; b.dataset.value=value;
    b.addEventListener('click',function(){
      if(kind==='cat'){ activeCat=value; } else { activeTag=value; }
      [].forEach.call(box.children,function(x){ x.classList.toggle('active', x.dataset.value===value); });
      render();
    });
    if(value==='all' && ((kind==='cat'&&activeCat==='all')||(kind==='tag'&&activeTag==='all'))) b.classList.add('active');
    box.appendChild(b);
  }
  chip('All chapters','all',catBox,'cat');
  model.chapters.forEach(function(c){ chip(c.title.replace(/^Chapter [IVX]+ — /,''), c.slug, catBox, 'cat'); });
  chip('Any tag','all',tagBox,'tag');
  ['vegetarian','vegan','dairy-free','gluten-free','quick','easy'].forEach(function(t){ chip(t,t,tagBox,'tag'); });
  function render(){
    var q = input.value.trim().toLowerCase();
    var terms = q ? q.split(/[,\\n]+/).map(function(s){return s.trim();}).filter(Boolean) : [];
    var hits = data.filter(function(r){
      if(activeCat!=='all' && r.chapter!==activeCat) return false;
      if(activeTag!=='all' && r.tags.indexOf(activeTag)<0) return false;
      return terms.every(function(t){ return matches(r,t); });
    });
    if(!terms.length && activeCat==='all' && activeTag==='all'){
      out.innerHTML = '<p class="muted">'+data.length+' recipes. Start typing an ingredient, or pick a chapter or tag above.</p>'; return;
    }
    if(!hits.length){ out.innerHTML = '<p class="notice">No recipes match. Try a shorter ingredient word or clear a filter.</p>'; return; }
    var html = '<p class="muted">'+hits.length+' recipe'+(hits.length===1?'':'s')+' match.</p>';
    html += hits.map(function(r){
      var matched = terms.length ? r.ingredients.filter(function(i){ return terms.some(function(t){ return i.toLowerCase().indexOf(t)>-1; }); }) : [];
      var listHtml = matched.length ? '<ul class="ingredients">'+matched.map(function(i){return '<li>'+esc(i)+'</li>';}).join('')+'</ul>' : '';
      var tags = r.tags.slice(1).map(function(t){return '<span class="tag">'+esc(t)+'</span>';}).join('');
      return '<article class="recipe-hit"><h3><a href="chapters/chapter'+String(r.chapterNumber).padStart(2,'0')+'.html#'+r.id+'">'+esc(r.title)+'</a></h3>'
        + '<p class="muted">'+esc(r.chapterTitle)+'</p>'+listHtml+'<p class="tagrow">'+tags+'</p></article>';
    }).join('');
    out.innerHTML = html;
  }
  var params = new URLSearchParams(location.search);
  if(params.get('q')) input.value = params.get('q');
  input.addEventListener('input', render);
  render();
})();
"""


def main():
    model = cm.build_model()
    for ci, c in enumerate(model["chapters"], 2):
        for r in c["recipes"]:
            r["chapterNumber"] = ci
    (ROOT / "data" / "recipes.json").write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding="utf-8")
    appendices = json.loads((ROOT / "data" / "appendices.json").read_text(encoding="utf-8"))
    build_manuscript(model, appendices)
    build_epub(model, appendices)
    build_print_edition(model, appendices)
    build_site(model, appendices)
    print(f"Built {sum(len(c['recipes']) for c in model['chapters'])} recipes across {len(model['chapters'])} chapters.")


if __name__ == "__main__":
    main()
