import re
from lib import *

SEALS = ['100 % Öko Anbau', 'Eigene Schlachtung', '100 % regionale Wertschöpfung', '100 % transparent', 'Familienbetrieb']
WA = 'https://wa.me/' + SITE['tel_href'].lstrip('+')

def build():
    s = 'hofeigene-schlachtung'
    plain = lambda x: re.sub(r'<[^>]+>', '', x)
    body = phero(blk(s, 0), blk(s, 1), 'Schlachterei · Spreewälder Rindfleisch',
                 img('rinder-herbst', 'Rinder der Rasse Blonde d’Aquitaine auf der Weide', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 800, 1200], pos='60% 50%'),
                 crumbs=[('Schlachterei', '/hofeigene-schlachtung/')], ratio='ar-45',
                 actions=btn('Termine & Vorbestellung', '#termine') + btn('Anrufen', 'tel:' + SITE['tel_href'], 'ghost', arrow=False))
    checks = ''.join(f'<li>{blk(s, i)}</li>' for i in range(3, 10))
    body += section(f'''
<div class="split split--top">
  <div class="prose">{reveal('<p>' + blk(s, 2) + '</p>')}</div>
  <div class="card reveal" style="--d:.1s"><ul class="checks">{checks}</ul></div>
</div>
<div class="seal-row reveal" style="margin-top:clamp(3rem,6vw,5rem)">{''.join(f'<div class="seal">{x}</div>' for x in SEALS)}</div>''')
    body += section(f'<div class="reveal"><div class="pic ar-31 pic--shadow">{img("steak", "Rindersteak mit Rosmarin auf einem Holzbrett", "100vw", widths=[640, 970], pos="50% 55%")}</div></div>', cls='section--tight')
    body += f'''<section class="section section--accent" id="termine" style="--accent:var(--burgund)">{wave('--burgund')}<div class="container"><div class="split split--wide-text split--top">
  <div>
    {reveal(countdown())}
    {reveal('<p style="font:400 1.2rem/1.6 var(--font-head);margin-top:2rem">Frisches Fleisch &amp; Wurstwaren vom Mutschenhof aus Lehde.</p>')}
    {reveal('<p>' + DATES['vorbestellung'] + '</p>')}
    {reveal(f'<div class="btn-row">{btn("Anrufen", "tel:" + SITE["tel_href"], "light", arrow=False)}{btn("WhatsApp schreiben", WA, "ghost-light", extra=" rel=noopener")}</div>')}
  </div>
  <div class="reveal" style="--d:.1s"><p class="eyebrow">Flyer Saison {DATES['saison']}</p>
    <div class="gallery gallery--even" style="grid-template-columns:repeat(2,1fr)">
      <a class="lb" style="aspect-ratio:1291/2560" href="{full('flyer-rindfleisch', 1280)}" data-group="flyer" data-alt="Flyer: Spreewälder Rindfleisch, Blonde d’Aquitaine aus Weidehaltung" data-caption="Spreewälder Rindfleisch – Blonde d’Aquitaine aus Weidehaltung">{img('flyer-rindfleisch', 'Flyer: Spreewälder Rindfleisch', '(max-width:860px) 45vw, 20vw', widths=[360, 640])}</a>
      <a class="lb" style="aspect-ratio:1291/2560" href="{full('flyer-termine', 1280)}" data-group="flyer" data-alt="Flyer: Schlachttermine 2025/26" data-caption="Schlachttermine {DATES['saison']}">{img('flyer-termine', 'Flyer: Schlachttermine 2025/26', '(max-width:860px) 45vw, 20vw', widths=[360, 640])}</a>
    </div></div>
</div></div></section>'''
    body += section(f'''
<div class="head">{eyebrow('Vom Hof')}<h2>Frisch geschlachtet, sorgfältig verarbeitet</h2></div>
<div class="reveal">{gallery([('wurst', 'Wurstwaren mit Gewürzen auf einem Holzbrett', 'Wurstwaren'), ('zerlegen', 'Fleisch wird im Schlachthaus zerlegt', 'Frisch geschlachtet'), ('salami', 'Salami, Brot, Frischkäse und Käse', 'Hofeigene Spezialitäten'), ('steak', 'Rindersteak mit Rosmarin', 'Rindfleisch')], 'produkte', even=True)}</div>''')
    body += section(f'''
<div class="head">{eyebrow('Die Rasse')}<h2>{blk(s, 10)}</h2></div>
<div class="split split--wide-media split--top">
  <div class="frame reveal"><div class="pic ar-43 pic--shadow">{img('rinder-wiese', 'Rinder der Herde am Fließ', '(max-width:860px) 92vw, 40vw', widths=[480, 800, 1080])}</div></div>
  <div class="stack">
    <article class="card reveal"><h3>{plain(blk(s, 12))}</h3><p>{blk(s, 13)}</p></article>
    <article class="card reveal"><h3>{plain(blk(s, 14))}</h3><p>{blk(s, 15)}</p></article>
    <article class="card reveal"><h3>{plain(blk(s, 16))}</h3><p>{blk(s, 17)}</p></article>
  </div>
</div>''', cls='section--alt', wave_top='--cream-2')
    body += more([('/artgerechte-tierhaltung/', 'Der Hof', 'Artgerechte Tierhaltung', 'Die Rinder wachsen in Mutterkuhhaltung auf und dürfen ihre Hörner behalten.'),
                  ('/hoffuehrung/', 'Erleben', 'Hofführung mit Verkostung', 'Zum Abschluss eine kleine Verkostung der hofeigenen Spezialitäten.'),
                  ('/kontakt/', 'Kontakt', 'Fragen zur Schlachterei?', 'Rufen Sie uns an oder schreiben Sie uns.')])
    return dict(slug=s, title='Schlachterei – Spreewälder Rindfleisch', desc=META[s]['desc'], body=body, og='rinder-herbst', theme='burgund')
