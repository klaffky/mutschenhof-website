#!/usr/bin/env python3
"""Prüft in dist/: interne Links, Anker, Bilder/Assets und doppelte IDs."""
import re, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
D = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if a.get('id'): s.ids.append(a['id'])
        for k in ('href','src','data-src'):
            if a.get(k): s.refs.append((t,k,a[k]))
        if a.get('srcset'):
            for part in a['srcset'].split(','): s.refs.append((t,'srcset',part.strip().split()[0]))
        if t=='link' and a.get('rel')=='preload': s.refs.append((t,'href',a['href']))
bad=0; pages={}
for f in D.rglob('*.html'):
    p=P(); p.feed(f.read_text(encoding='utf8')); pages[f]=p
    dups={i for i in p.ids if p.ids.count(i)>1}
    if dups: print('DUP IDS',f,dups); bad+=1
for f,p in pages.items():
    for t,k,u in p.refs:
        if u.startswith(('http:','https:','mailto:','tel:','data:','javascript:')): continue
        pu=urlparse(u); path=unquote(pu.path)
        tgt=(D/path.lstrip('/')) if path else f
        if path.endswith('/'): tgt=tgt/'index.html'
        if path=='' : tgt=f
        if not tgt.exists(): print('MISSING',f.relative_to(D),k,u); bad+=1; continue
        if pu.fragment and tgt.suffix=='.html':
            ids=pages.get(tgt).ids if tgt in pages else []
            if pu.fragment not in ids: print('NO ANCHOR',f.relative_to(D),u); bad+=1
print('Seiten:',len(pages),'Probleme:',bad)
