#!/usr/bin/env python3
"""Baut die Website nach dist/ (nur Python 3 + Pillow nötig).
   Aufruf:  python3 build.py        Vorschau:  python3 -m http.server 8000 -d dist"""
import importlib, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'site'))
import lib
from lib import DIST, SRC, SITE, render, write_images
from PIL import Image

MODULES = ['p_home', 'p_hof', 'p_wohnen', 'p_erleben', 'p_schlachterei', 'p_besuch']

def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    pages = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                print('übersprungen:', m); continue
            raise
        r = mod.build()
        pages += r if isinstance(r, list) else [r]
    for p in pages:
        out = DIST / (p['slug'] + '/index.html' if p['slug'] else 'index.html')
        if p['slug'] == '404':
            out = DIST / '404.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(p), encoding='utf8')
    n = write_images()
    shutil.copytree(SRC / 'assets' / 'fonts', DIST / 'assets' / 'fonts')
    # Favicons aus dem Logo
    logo = Image.open(SRC / 'assets' / 'img-src' / 'logo.png').convert('RGBA')
    for size, name in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png')):
        canvas = Image.new('RGBA', (size, size), (246, 241, 227, 255))
        l = logo.copy(); l.thumbnail((int(size * .86),) * 2)
        canvas.alpha_composite(l, ((size - l.width) // 2, (size - l.height) // 2))
        canvas.convert('RGB').save(DIST / name)
    urls = [p for p in pages if p['slug'] != '404' and not p.get('noindex')]
    sm = ''.join(f"<url><loc>{SITE['url']}{'/' if not p['slug'] else '/' + p['slug'] + '/'}</loc></url>" for p in urls)
    (DIST / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sm + '</urlset>')
    (DIST / 'robots.txt').write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f'{len(pages)} Seiten, {n} Bilddateien → {DIST}')

if __name__ == '__main__':
    main()
