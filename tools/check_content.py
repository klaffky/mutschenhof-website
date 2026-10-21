#!/usr/bin/env python3
"""Vergleicht die Texte der alten Seite (WP-Spiegel) mit der neuen Seite: meldet Textstücke, die fehlen."""
import re, sys, html
from html.parser import HTMLParser
from pathlib import Path
OLD = Path(sys.argv[1]); NEW = Path(sys.argv[2])
norm = lambda t: re.sub(r'\s+', ' ', html.unescape(t)).replace('’', "'").replace('‘', "'").replace('„', '"').replace('“', '"').replace('–', '-').replace(' ', ' ').strip().lower()
class T(HTMLParser):
    def __init__(s, main_id=None): super().__init__(convert_charrefs=True); s.t=[]; s.skip=0; s.on=main_id is None; s.id=main_id
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style','noscript','svg','form','select','option','button'): s.skip+=1
        if s.id and a.get('id')==s.id: s.on=True
        if t=='br': s.t.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript','svg','form','select','option','button'): s.skip-=1
        if t in('p','div','li','h1','h2','h3','h4','section','ul'): s.t.append('\n')
    def handle_data(s,d):
        if s.on and not s.skip: s.t.append(d)
def text(path, main=None):
    p=T(main); p.feed(path.read_text(encoding='utf8',errors='replace')); return ''.join(p.t)
new_all = norm(' '.join(text(f) for f in NEW.rglob('*.html')))
SKIP = ('your content goes here','cookie','zustimmung','verwalten','einstellungen','lieferanten','{title}','vendor_count','funktional','vorlieben','statistiken','marketing','technische speicherung','technische speicherung','akzeptieren','searching availability','tag(e)','stunde(n)','minute(n)','sekunde(n)')
miss = 0; total = 0
for f in sorted(OLD.glob('*/index.html')) + [OLD/'index.html']:
    raw = text(f, 'et-main-area')
    raw = raw.split('MUTSCHENHOF UG')[0]
    for line in raw.split('\n'):
        for part in re.split(r'(?<=[.!?])\s+', line):
            n = norm(part)
            if len(n) < 28 or any(k in n for k in SKIP): continue
            total += 1
            if n not in new_all:
                miss += 1; print('FEHLT', f.parent.name or 'home', '|', part.strip()[:140])
print(f'geprüfte Satzstücke: {total}, nicht gefunden: {miss}')
