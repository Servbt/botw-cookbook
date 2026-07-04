from pathlib import Path
import re, html, shutil

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
    top = f'<a href="{depth}index.html">Contents</a><a href="{depth}book/The_Wild_Table.epub">Download EPUB</a>'
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

index_body = '<h1>The Wild Table</h1>\n<div class="notice"><strong>Unofficial fan work:</strong> Original prose and real-world recipe adaptations. No official art, logos, or screenshots.</div>\n<h2>Contents</h2>\n<ol>' + ''.join(f'<li><a href="{href}">{html.escape(title)}</a></li>' for _, title, href in entries) + '</ol>'
(docs / 'index.html').write_text(page('Contents', index_body, None, ''), encoding='utf-8')

for idx, p in enumerate(chapters, 1):
    x = p.read_text(encoding='utf-8')
    content = body_inner(x)
    content = re.sub(r'href="chapter(\d{2})\.xhtml"', r'href="chapter\1.html"', content)
    title = entries[idx - 1][1]
    (docs / 'chapters' / f'chapter{idx:02d}.html').write_text(page(title, content, idx, '../'), encoding='utf-8')

(docs / '.nojekyll').write_text('', encoding='utf-8')
print(f'Created GitHub Pages static site in {docs}')
print('Pages:', len(list((docs / 'chapters').glob('*.html'))) + 1)
for _, title, href in entries:
    print(f'- {title} -> {href}')
