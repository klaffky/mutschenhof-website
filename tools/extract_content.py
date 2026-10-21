#!/usr/bin/env python3
"""Liest die Texte der alten WordPress-Seite (Spiegel in /home/claude/src) in site/content.json.
Nur zur Übernahme der Originaltexte; wird für den normalen Build nicht benötigt."""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/src')
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else 'site/content.json')
SLUGS = ['der-mutschenhof','oekologische-landwirtschaft','artgerechte-tierhaltung','ferienwohnungen',
         'kahnfahrten','rent-a-kahn','hoffuehrung','hofeigene-schlachtung','freiwilliges-oekologisches-jahr-foej',
         'tipps-fuer-den-aufenthalt','wegbeschreibung','kontakt','impressum','datenschutz']
LINKMAP = {'index.html?p=722':'/kontakt/','index.html?p=188':'/rent-a-kahn/'}
KEEP = {'a','strong','em','b','i','br'}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.blocks=[]; s.cur=None; s.skip=0; s.main=False; s.stop=False; s.depth=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style','noscript','form','svg','iframe','button','select','option','textarea'): s.skip+=1; return
        if a.get('id')=='main-footer': s.stop=True
        if a.get('id')=='et-main-area': s.main=True
        if not s.main or s.stop or s.skip: return
        if t in('h1','h2','h3','h4','p','li') and s.cur is None:
            s.cur={'t':t,'x':''}; s.depth=0
        elif s.cur is not None and t in KEEP:
            if t=='a':
                h=a.get('href','')
                h=LINKMAP.get(h.split('../')[-1],h)
                s.cur['x']+=f'<a href="{h}">'
            else: s.cur['x']+=f'<{t}>' if t!='br' else '<br>'
    def handle_endtag(s,t):
        if t in('script','style','noscript','form','svg','iframe','button','select','option','textarea'): s.skip-=1; return
        if s.cur is not None:
            if t==s.cur['t']:
                x=re.sub(r'\s+',' ',s.cur['x']).strip()
                if re.sub(r'<[^>]+>','',x).strip(): s.blocks.append({'t':s.cur['t'],'x':x})
                s.cur=None
            elif t in KEEP and t!='br': s.cur['x']+=f'</{t}>'
    def handle_data(s,d):
        if s.cur is not None and not s.skip: s.cur['x']+=d.replace('&','&amp;').replace('<','&lt;')

out={}
for slug in SLUGS:
    p=P(); p.feed((SRC/slug/'index.html').read_text(encoding='utf8',errors='replace'))
    b=p.blocks
    for i,x in enumerate(b):
        if x['x'].startswith('MUTSCHENHOF UG'): b=b[:i]; break
    out[slug]=b
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf8')
for slug,b in out.items():
    print('=====',slug,len(b))
    for i,x in enumerate(b): print(i,x['t'],x['x'][:90].replace('\n',' '))
