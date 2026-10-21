from lib import *

LISCHKA = [('lischka-terrasse', 'Terrasse vor dem Blockhaus mit Sitzgruppe', 'Terrasse'),
           ('lischka-hof', 'Hof zwischen Blockhaus und Scheune', 'Hof'),
           ('lischka-esszimmer', 'Wohnbereich mit Couch und Essecke', 'Wohn- und Essbereich'),
           ('lischka-esszimmer-2', 'Gedeckter Esstisch und Schlafcouch', 'Essbereich'),
           ('lischka-kueche', 'Küche mit Holzwand', 'Küche'),
           ('lischka-schlafzimmer', 'Wohnraum mit Kachelofen und Schlafcouch', 'Wohnraum mit Kachelofen'),
           ('lischka-schlafzimmer-2', 'Schlafzimmer mit weißem Holzbett', 'Schlafzimmer'),
           ('lischka-schlafzimmer-3', 'Zimmer mit Sesseln und Schlafcouch', 'Zimmer')]
SPREEWA = [('spreewa-terrasse', 'Terrasse mit Sitzgruppe am Blockhaus', 'Terrasse'),
           ('spreewa-esszimmer', 'Essplatz mit Schlafcouch', 'Essbereich'),
           ('spreewa-kueche', 'Küche mit Holzwand und Blick in den Garten', 'Küche'),
           ('spreewa-schlafzimmer', 'Schlafzimmer mit dunklem Holzbett', 'Schlafzimmer'),
           ('spreewa-schlafzimmer-2', 'Zweites Zimmer mit Bett und Schlafcouch', 'Zimmer')]

def build():
    s = 'ferienwohnungen'
    ext = [x.strip() for x in strip_head(blk(s, 12)).split('<br>')] + ['Ihr eigener Kahn zum Übersetzen auf das Festland (kostenfreie Nutzung)']
    body = phero('Unsere beiden Ferienwohnungen', blk(s, 1), 'Ferienwohnungen · Lehde',
                 img('lischka-terrasse', 'Terrasse vor dem Blockbohlenhaus', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 510]),
                 crumbs=[('Ferienwohnungen', '/ferienwohnungen/')], ratio='ar-43',
                 actions=btn('Verfügbarkeit prüfen', '/buchungskalendar/') + btn('Anfahrt', '/wegbeschreibung/', 'ghost'))
    body += section(f'''
<div class="split split--wide-text">
  <div class="prose">{reveal(eyebrow('Das Haus'))}{reveal('<h2>' + blk(s, 3) + '</h2>')}{reveal(paras(s, 4, 7))}</div>
  <div class="media-stack reveal" style="--d:.1s">
    <div class="frame"><div class="pic ar-43 pic--shadow">{img('lischka-hof', 'Hof mit Sitzgruppe zwischen Blockhaus und Scheune', '(max-width:860px) 90vw, 40vw', widths=[360, 510])}</div></div>
    <div class="pic pic--float ar-43">{img('spreewa-terrasse', 'Terrasse am Blockhaus', '22vw', widths=[360, 510])}</div>
  </div>
</div>''')
    body += section(f'''
<div class="head">{eyebrow('Zwei Wohnungen')}<h2>Fewo Lischka &amp; Fewo Spreewa</h2></div>
<div class="stack" style="margin-bottom:4rem">
  <div class="split split--top"><div><h3>Fewo Lischka <span class="pill">Landhaus-Stil</span></h3>{gallery(LISCHKA, 'lischka')}</div>
  <div><h3>Fewo Spreewa <span class="pill">Rustikal</span></h3>{gallery(SPREEWA, 'spreewa')}</div></div>
</div>
<div class="split split--top">
  <div class="prose">
    <h2>Ausstattung</h2>
    <p>Unsere Ferienwohnungen sind 2016 komplett saniert und zeitgemäß ausgestattet worden. Jede FeWo hat 2 kombinierte Wohn- / Schlafräume für 4 Personen. (auf Anfrage Aufbettung möglich)</p>
    <div class="btn-row">{btn('Verfügbarkeit prüfen', '/buchungskalendar/')}{btn('Zur Anfahrt (Google Maps)', SITE['maps_hof'], 'ghost', extra=' rel="noopener"')}</div>
  </div>
  <div class="card">
    <dl class="dl">
      <div><dt>Küche</dt><dd>{strip_head(blk(s, 8))}</dd></div>
      <div><dt>Bad</dt><dd>{strip_head(blk(s, 9))}</dd></div>
      <div><dt>Wohnbereich</dt><dd>{strip_head(blk(s, 10))}</dd></div>
      <div><dt>Schlafbereich</dt><dd>{strip_head(blk(s, 11))}</dd></div>
      <div><dt>Extras</dt><dd><ul>{''.join(f'<li>{e}</li>' for e in ext)}</ul></dd></div>
    </dl>
  </div>
</div>''', cls='section--alt', wave_top='--cream-2')
    body += more([('/kahnfahrten/', 'Erleben', 'Hof-Kahnfahrten', 'Romantischer geht es nicht.'),
                  ('/tipps-fuer-den-aufenthalt/', 'Besuch', 'Tipps für den Aufenthalt', 'Der Spreewald und Ausflugsmöglichkeiten.'),
                  ('/der-mutschenhof/', 'Der Hof', 'Geschichte & Familie', 'Der Mutschenhof in fünfter Generation.')])
    p1 = dict(slug=s, title='Ferienwohnungen', desc=META[s]['desc'], body=body, og='lischka-terrasse')

    # ---------------------------------------------------------------- Buchungskalender
    s = 'buchungskalendar'
    def cal(anchor, name, id_, bg):
        return (f'<div id="{anchor}" class="reveal"><h3>{name}</h3>' +
                embed(f'https://www.fungiwo.com/extern/belegungskalender-einzel.php?id={id_}&sprache=deutsch', f'Belegungskalender {name}',
                      'Kalender laden', bg_key=bg, light=False, tall=True,
                      text='Der Kalender wird vom Dienst fungiwo.de bereitgestellt. Erst mit Ihrem Klick wird er geladen und dabei Daten (z. B. Ihre IP-Adresse) an fungiwo übertragen.') + '</div>')
    body = phero('Buchungskalender', META[s]['desc'], 'Ferienwohnungen', img('lischka-schlafzimmer-2', 'Schlafzimmer mit weißem Holzbett', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 510]),
                 crumbs=[('Ferienwohnungen', '/ferienwohnungen/')], ratio='ar-43')
    body += section(f'''<div class="split split--top">{cal('ankerlischka', 'Fewo Lischka', 17281387, 'lischka-schlafzimmer')}{cal('ankerspreewa', 'Fewo Spreewa', 17284262, 'spreewa-schlafzimmer')}</div>''')
    body += section(f'''<div class="head" id="ankerbuchung">{eyebrow('Anfrage')}<h2>Buchung anfragen</h2></div>
<div class="reveal">{embed('https://www.fungiwo.com/extern/anfrage.php?id=17281387&sprache=deutsch', 'Buchungsanfrage', 'Anfrageformular laden', bg_key='lischka-esszimmer', light=True, tall=True,
 text='Das Anfrageformular wird vom Dienst fungiwo.de bereitgestellt und erst nach Ihrem Klick geladen.')}</div>
<p class="center" style="margin-top:1.5rem">Lieber persönlich? Rufen Sie uns an unter <a class="link" href="tel:{SITE["tel_href"]}">{SITE["tel"]}</a> oder schreiben Sie an <a class="link" href="mailto:{SITE["mail"]}">{SITE["mail"]}</a>.</p>''', cls='section--alt', wave_top='--cream-2')
    p2 = dict(slug=s, title='Buchungskalender', desc=META[s]['desc'], body=body, og='lischka-schlafzimmer-2')
    return [p1, p2]
