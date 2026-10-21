#!/usr/bin/env python3
"""Erzeugt aus dist/ eine Vorschau-Kopie in docs/ für GitHub Pages (Projektadresse mit Unterordner).
Alle Pfade werden relativ gemacht, Verzeichnislinks zeigen auf index.html, und die Seiten erhalten noindex.
Für die echte Domain wird NICHT docs/, sondern dist/ hochgeladen.   Aufruf: python3 build.py && python3 tools/make_preview.py"""
import re, shutil, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
SRC, DST = R / 'dist', R / 'docs'
if DST.exists(): shutil.rmtree(DST)
shutil.copytree(SRC, DST)
(DST / '.nojekyll').write_text('')
(DST / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(DST / 'sitemap.xml').unlink(missing_ok=True)

def rel(p, depth):
    pre = '../' * depth if depth else './'
    m = re.match(r'([^?#]*)([?#].*)?$', p); path, q = m.group(1).lstrip('/'), m.group(2) or ''
    if path == '' or path.endswith('/'): path += 'index.html'
    return pre + path + q

for f in DST.rglob('*'):
    if not f.is_file(): continue
    d = len(f.relative_to(DST).parts) - 1
    if f.suffix == '.html':
        s = f.read_text(encoding='utf8')
        s = re.sub(r'((?:href|src|poster|data-src)=")(/[^"]*)"', lambda m: m.group(1) + rel(m.group(2), d) + '"', s)
        def ss(m):
            out = []
            for x in [x.strip() for x in m.group(2).split(',')]:
                u, *r = x.split(' ')
                out.append(' '.join([rel(u, d) if u.startswith('/') else u] + r))
            return m.group(1) + ', '.join(out) + '"'
        s = re.sub(r'(srcset=")([^"]*)"', ss, s)
        s = re.sub(r'(data-[a-z]+=")(/[^"]*\.(?:webp|jpg|png))"', lambda m: m.group(1) + rel(m.group(2), d) + '"', s)
        s = s.replace('<head>', '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
        f.write_text(s, encoding='utf8')
    elif f.suffix == '.css':
        s = f.read_text(encoding='utf8')
        f.write_text(re.sub(r'url\(\s*([\'"]?)/([^)\'"]*)\1\s*\)', lambda m: 'url(../' + m.group(2) + ')', s), encoding='utf8')
print('Vorschau →', DST)
