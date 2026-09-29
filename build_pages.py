from pathlib import Path
import re, html, shutil, json
import search_index

root = Path('/home/arian/botw-cookbook')
oebps = root / 'book/epub_build/OEBPS'
docs = root / 'docs'
chapters = [oebps / f'chapter{i:02d}.xhtml' for i in range(1, 13)]
assert all(p.exists() for p in chapters), 'Missing chapter files'

docs.mkdir(exist_ok=True)
(docs / 'chapters').mkdir(exist_ok=True)
(docs / 'styles').mkdir(exist_ok=True)

css = """
:root {
  --bg: #fffaf0;
  --paper: #fffdf7;
  --ink: #24170f;
  --muted: #6f5946;
  --accent: #b56a1d;
  --accent-dark: #7a4218;
  --line: #e2c9a6;
  --nav: #2f1c10;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Georgia, 'Times New Roman', serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.6;
}
a { color: var(--accent-dark); }
.layout { display: grid; grid-template-columns: 300px minmax(0, 1fr); min-height: 100vh; }
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  padding: 28px 22px;
  background: var(--nav);
  color: #f7ead5;
  border-right: 1px solid rgba(255,255,255,.08);
}
.sidebar h1 { font-size: 1.35rem; margin: 0 0 .35rem; line-height: 1.15; }
.sidebar .subtitle { margin: 0 0 1.4rem; color: #d9c6a9; font-size: .9rem; }
.sidebar nav { display: grid; gap: .35rem; }
.sidebar a {
  color: #f7ead5;
  text-decoration: none;
  display: block;
  padding: .55rem .65rem;
  border-radius: 10px;
  border: 1px solid transparent;
}
.sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,.08); border-color: rgba(255,255,255,.12); }
.content { max-width: 920px; width: 100%; padding: 48px 38px 96px; margin: 0 auto; background: var(--paper); }
.toplinks { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; color: var(--muted); }
h1 { font-size: clamp(2.1rem, 5vw, 3.3rem); color: #5a2f12; border-bottom: 3px solid var(--accent); padding-bottom: .35rem; margin-top: 0; }
h2 { font-size: 1.55rem; color: var(--accent-dark); margin-top: 2rem; }
h3 { font-size: 1.35rem; color: #3b2415; margin-top: 2.2rem; border-top: 1px solid var(--line); padding-top: 1.2rem; }
p, li { font-size: 1.03rem; }
strong { color: #3a2112; }
code { background: #f4e7d2; padding: 0 .25em; border-radius: 3px; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2rem 0; }
ul, ol { padding-left: 1.4rem; }
.chapter-nav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; padding-top: 1.25rem; border-top: 1px solid var(--line); }
.chapter-nav a { text-decoration: none; font-weight: bold; }
.notice { background:#f7ead5; border:1px solid var(--line); padding:1rem; border-radius:12px; }
.muted { color: var(--muted); }
.search-box { margin: 0 0 1.5rem; }
.search-box label { display:block; font-weight:bold; margin-bottom:.4rem; color:#3a2112; }
#pantry-input { width:100%; padding:.8rem 1rem; font-size:1.1rem; font-family:inherit; border:2px solid var(--accent); border-radius:10px; background:var(--paper); color:var(--ink); }
#pantry-input:focus { outline:none; box-shadow:0 0 0 3px rgba(181,106,29,.25); }
.recipe-hit { border-top:1px solid var(--line); padding-top:1rem; margin-top:1rem; }
.recipe-hit h3 { margin-top:0; border-top:0; padding-top:0; }
.recipe-hit h3 a { text-decoration:none; }
.recipe-hit .ingredients { margin:.3rem 0 0; color:var(--muted); }
@media (max-width: 860px) {
  .layout { display: block; }
  .sidebar { position: relative; height: auto; }
  .sidebar nav { grid-template-columns: 1fr; }
  .content { padding: 32px 20px 72px; }
  .toplinks, .chapter-nav { flex-direction: column; }
}
@media print {
  .sidebar, .toplinks, .chapter-nav { display:none; }
  .layout { display:block; }
  .content { padding:0; max-width:none; }
  body { background:white; }
}
""".strip()
(docs / 'styles/site.css').write_text(css, encoding='utf-8')

entries = []
for idx, p in enumerate(chapters, 1):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S | re.I)
    title = re.sub('<.*?>', '', m.group(1)).strip() if m else f'Chapter {idx}'
    entries.append((idx, title, f'chapters/chapter{idx:02d}.html'))

def body_inner(xhtml: str) -> str:
    m = re.search(r'<body[^>]*>(.*?)</body>', xhtml, re.S | re.I)
    return m.group(1).strip() if m else xhtml

def page(title: str, body: str, current_idx=None, depth='') -> str:
    links = []
    for idx, t, href in entries:
        rel = depth + href
        cls = ' class="active"' if idx == current_idx else ''
        links.append(f'<a{cls} href="{rel}">{html.escape(t)}</a>')
    nav = '\n        '.join(links)
    nav += f'\n        <a href="{depth}search.html">Search by ingredient</a>'
    top = f'<a href="{depth}index.html">Contents</a><a href="{depth}search.html">Search</a><a href="{depth}book/The_Wild_Table.epub">Download EPUB</a>'
    prev_next = ''
    if current_idx:
        if current_idx > 1:
            prev_link = f'<a href="chapter{current_idx-1:02d}.html">← {html.escape(entries[current_idx-2][1])}</a>'
        else:
            prev_link = '<a href="../index.html">← Contents</a>'
        next_link = ''
        if current_idx < len(entries):
            next_link = f'<a href="chapter{current_idx+1:02d}.html">{html.escape(entries[current_idx][1])} →</a>'
        prev_next = f'<div class="chapter-nav"><div>{prev_link}</div><div>{next_link}</div></div>'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · The Wild Table</title>
  <link rel="stylesheet" href="{depth}styles/site.css">
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h1>The Wild Table</h1>
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

(docs / 'book').mkdir(exist_ok=True)
shutil.copy2(root / 'book/The_Wild_Table.epub', docs / 'book/The_Wild_Table.epub')

index_body = '<h1>The Wild Table</h1>\n<div class="notice"><strong>Unofficial fan work:</strong> Original prose and real-world recipe adaptations. No official art, logos, or screenshots.</div>\n<p><a href="search.html"><strong>🔍 Search by ingredient</strong></a> — type what is in your pantry and every matching recipe appears.</p>\n<h2>Contents</h2>\n<ol>' + ''.join(f'<li><a href="{href}">{html.escape(title)}</a></li>' for _, title, href in entries) + '</ol>'
(docs / 'index.html').write_text(page('Contents', index_body, None, ''), encoding='utf-8')

def add_anchors(content: str) -> str:
    def repl(m):
        inner = m.group(1)
        title = re.sub('<.*?>', '', inner).strip()
        return f'<h3 id="{search_index.slugify(title)}">{inner}</h3>'
    return re.sub(r'<h3[^>]*>(.*?)</h3>', repl, content, flags=re.S | re.I)

for idx, p in enumerate(chapters, 1):
    x = p.read_text(encoding='utf-8')
    content = body_inner(x)
    content = re.sub(r'href="chapter(\d{2})\.xhtml"', r'href="chapter\1.html"', content)
    content = add_anchors(content)
    title = entries[idx - 1][1]
    (docs / 'chapters' / f'chapter{idx:02d}.html').write_text(page(title, content, idx, '../'), encoding='utf-8')

# Pantry-ingredient search page backed by the recipe index.
recipe_index = search_index.extract_recipes(oebps)
index_json = json.dumps(recipe_index, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

search_js = """
(function(){
  var data = JSON.parse(document.getElementById('recipe-index').textContent);
  var input = document.getElementById('pantry-input');
  var out = document.getElementById('results');
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function matches(recipe,t){
    if(recipe.title.toLowerCase().indexOf(t)>-1) return true;
    return recipe.ingredients.some(function(i){return i.toLowerCase().indexOf(t)>-1;});
  }
  function render(){
    var q = input.value.trim().toLowerCase();
    if(!q){ out.innerHTML = '<p class="muted">Start typing an ingredient you have on hand \u2014 for example <em>cabbage</em>, <em>egg</em>, <em>mushroom</em>, or <em>tomato</em>.</p>'; return; }
    var terms = q.split(/[,\\n]+/).map(function(s){return s.trim();}).filter(Boolean);
    var hits = data.filter(function(r){ return terms.every(function(t){ return matches(r,t); }); });
    if(!hits.length){ out.innerHTML = '<p class="notice">No recipes match \u201c'+esc(q)+'\u201d. Try a shorter ingredient word.</p>'; return; }
    var html = '<p class="muted">'+hits.length+' recipe'+(hits.length===1?'':'s')+' match.</p>';
    html += hits.map(function(r){
      var matched = r.ingredients.filter(function(i){ return terms.some(function(t){ return i.toLowerCase().indexOf(t)>-1; }); });
      var listHtml = matched.length ? '<ul class="ingredients">'+matched.map(function(i){return '<li>'+esc(i)+'</li>';}).join('')+'</ul>' : '';
      return '<article class="recipe-hit"><h3><a href="'+r.href+'#'+r.anchor+'">'+esc(r.title)+'</a></h3><p class="muted">'+esc(r.chapter)+'</p>'+listHtml+'</article>';
    }).join('');
    out.innerHTML = html;
  }
  input.addEventListener('input', render);
  render();
})();
"""

search_body = (
    '<h1>Search by ingredient</h1>'
    '<div class="notice">Type an ingredient you have on hand and every matching recipe appears. '
    'Separate several ingredients with commas to narrow it down (e.g. <em>egg, mushroom</em>).</div>'
    '<div class="search-box"><label for="pantry-input">Your pantry ingredients</label>'
    '<input id="pantry-input" type="search" placeholder="cabbage, egg, mushroom\u2026" autocomplete="off"></div>'
    '<div id="results" aria-live="polite"></div>'
    f'<script id="recipe-index" type="application/json">{index_json}</script>'
    f'<script>{search_js}</script>'
)
(docs / 'search.html').write_text(page('Search by ingredient', search_body, None, ''), encoding='utf-8')

(docs / '.nojekyll').write_text('', encoding='utf-8')
print(f'Created GitHub Pages static site in {docs}')
print('Pages:', len(list((docs / 'chapters').glob('*.html'))) + 1)
print(f'Search index: {len(recipe_index)} recipes')
for _, title, href in entries:
    print(f'- {title} -> {href}')
