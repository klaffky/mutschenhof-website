import re
from lib import *

def pf(key, alt, ratio='ar-43', sizes='(max-width:860px) 92vw, 46vw', widths=(480, 800, 1200), **kw):
    return f'<div class="frame"><div class="pic {ratio} pic--shadow">{img(key, alt, sizes, widths=list(widths), **kw)}</div></div>'

def plain(x):
    return re.sub(r'<[^>]+>', '', x).replace('&amp;', '&')

def build():
    pages = []

    # ---------------------------------------------------------------- Kahnfahrten
    s = 'kahnfahrten'
    g = [('fliess-gruen', 'Ein grünes Spreewaldfließ', 'Spreewaldfließ'), ('kahn-staker', 'Kahn mit Stakerin auf dem Fließ', 'Unterwegs im Kahn'),
         ('kuhweide', 'Rinder grasen am Wasser', 'Rinder am Ufer'), ('kahn-hof', 'Kahn mit Gästen vor dem Haus', 'Am Hof'),
         ('natur-baeume', 'Baumreihe am Wasser', 'Spreewaldnatur'), ('kahn-paar', 'Zwei Gäste im Kahn', 'Zwei Gäste im Kahn')]
    body = phero('Kahnfahrten vom Mutschenhof', blk(s, 1).replace('<br>', ''), 'Erleben · Lehde', img('kahn-paar', 'Zwei Gäste im Kahn, hinter ihnen steht die Stakerin', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 540], pos='50% 40%'),
                 crumbs=[('Erleben', '/kahnfahrten/')], ratio='ar-43', actions=btn('Kahnfahrt anfragen', '#anfrage') + btn('Selbst staken', '/rent-a-kahn/', 'ghost'))
    body += section(f'''
<div class="head">{eyebrow('Unterwegs')}<h2>Unterwegs im Herzen des Spreewaldes</h2><p class="lede">{blk(s, 2).replace('unterwegs im Herzen des Spreewaldes ', '', 1)}</p></div>
<div class="reveal">{gallery(g, 'kahn', cols=3)}</div>''')
    t4 = blk(s, 4).split('<br>')[0]
    t5 = re.sub(r'href="[^"]*#kontakt"', 'href="#anfrage"', blk(s, 5))
    body += section(f'''
<div class="split split--top">
  <div class="prose">{reveal('<h2>Individuelle Kahnfahrten</h2>')}{reveal('<p>' + t4 + '</p>')}{reveal('<p class="price"><b>ab 105&nbsp;€</b><span>pro Stunde</span></p>')}{reveal('<p>' + t5 + '</p>')}</div>
  <div class="card reveal" style="--d:.1s">
    <dl class="dl">
      <div><dt>Tage</dt><dd>Kahnfahrten nur Dienstag, Donnerstag und Samstag möglich oder nach individueller Absprache</dd></div>
      <div><dt>Startzeiten</dt><dd>9.30 Uhr · 10.00 Uhr · 11.00 Uhr · individuell</dd></div>
      <div><dt>Personen</dt><dd>bereits ab zwei Personen buchbar</dd></div>
      <div><dt>Zusatzoptionen</dt><dd><ul><li>selbstgemachtes Schmalzbrot (2&nbsp;€ pro Person)</li><li>Gurkenmix von der Gurkeneinlegerei Nissel (4,50&nbsp;€ pro Person)</li><li>Rundgang über unseren Mutschenhof (5,00&nbsp;€ pro Person)</li></ul></dd></div>
    </dl>
  </div>
</div>''', cls='section--alt', wave_top='--cream-2')
    fm = form('Anfrage Kahnfahrt',
              '<div class="row">' + f_select('anrede', 'Anrede', ['Herr', 'Frau', 'Divers', 'Familie', 'Gruppe'], placeholder='bitte auswählen') + f_text('name', 'Name', req=True, extra='autocomplete="name"') + '</div>'
              '<div class="row">' + f_text('email', 'E-Mail', 'email', True, 'autocomplete="email"') + f_text('tel', 'Telefonnummer', 'tel', True, 'autocomplete="tel"') + '</div>'
              + f_choice('reise', 'Art der Reise', ['geschäftlich', 'privat'], req=True) +
              '<div class="row">' + f_text('tag', 'Tag der Kahnfahrt', 'date', True, 'data-weekdays="2,4,6"', 'Bitte beachten: Kahnfahrten nur Dienstag, Donnerstag und Samstag möglich oder nach individueller Absprache') + f_select('startzeit', 'Gewünschte Startzeit', ['9.30 Uhr', '10.00 Uhr', '11.00 Uhr', 'individuell'], req=True) + '</div>'
              '<p class="hint" id="day-hint" hidden>Dieser Tag liegt außerhalb der üblichen Fahrtage (Di, Do, Sa) – das ist nach individueller Absprache möglich.</p>'
              '<div class="row">' + f_stepper('personen', 'Teilnehmeranzahl') + f_stepper('kinder', 'davon Kinder (bis 12 Jahre)') + '</div>'
              + f_choice('zusatz', 'Gewünschte Zusatzoption', ['selbstgemachtes Schmalzbrot (2 € pro Person)', 'Gurkenmix von der Gurkeneinlegerei Nissel (4,50 € pro Person)', 'Rundgang über unseren Mutschenhof (5,00 € pro Person)'], kind='checkbox')
              + f_area('wuensche', 'Ihre Fragen und Wünsche', True))
    body += section(f'<div class="split split--top"><div class="head" style="margin:0">{eyebrow("Anfrage")}<h2>Kahnfahrt anfragen</h2><p class="lede">Sagen Sie uns Ihren Wunschtermin – wir melden uns bei Ihnen.</p><div class="frame" style="margin-top:2rem;max-width:30rem"><div class="pic ar-43 pic--shadow">{img("kahn-hof", "Kahn mit Gästen vor dem Haus", "30rem", widths=[480, 540])}</div></div></div><div class="card">{fm}</div></div>', id='anfrage')
    pages.append(dict(slug=s, title='Kahnfahrten', desc=META[s]['desc'], body=body, og='kahn-paar'))

    # ---------------------------------------------------------------- Rent a Kahn
    s = 'rent-a-kahn'
    vid = embed('https://www.youtube-nocookie.com/embed/4tBkLqZm9_E', 'Video: Rent a Kahn, drive alone', 'Video laden', bg_key='fliess-2', video=True,
                text='Das Video wird von YouTube bereitgestellt. Erst mit Ihrem Klick wird es geladen und dabei Daten (z. B. Ihre IP-Adresse) an YouTube/Google übertragen.')
    body = phero('Rent a Kahn, drive alone', '', 'Erleben · Kahnfahrschule & Verleih', img('fliess-2', 'Spiegelndes Fließ zwischen kahlen Bäumen', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 800, 970], pos='50% 50%'),
                 crumbs=[('Erleben', '/kahnfahrten/')], ratio='ar-45', actions=btn('Kontakt aufnehmen', '/kontakt/'))
    body = body.replace('<p class="lede"></p>', '')
    body += section(f'''
<div class="prose" style="max-width:48rem;margin-inline:auto">{reveal('<p class="lede">' + blk(s, 1) + '</p>')}</div>''', cls='section--tight', narrow=True)
    body += section(rows([
        (plain(blk(s, 2)), '<p>' + blk(s, 3) + '</p>', vid),
        (plain(blk(s, 4)), '<p>' + blk(s, 5) + '</p>', pf('kahn-staker', 'Stakerin im Kahn auf einem Fließ')),
        (plain(blk(s, 6)), '<p>' + blk(s, 7) + '</p>', pf('fliess-3', 'Ein stilles, grünes Fließ')),
    ]), cls='')
    body += section(f'''<div class="cards">
 <article class="card reveal"><h3>{plain(blk(s, 8))}</h3><p>{blk(s, 9)}</p>{btn('Kontakt aufnehmen', '/kontakt/')}</article>
 <article class="card reveal" style="--d:.1s"><h3>{plain(blk(s, 10))}</h3><p>{blk(s, 11)}</p>{btn('Gutschein anfragen', '/kontakt/', 'ghost')}</article></div>''', cls='section--alt', wave_top='--cream-2')
    pages.append(dict(slug=s, title='Rent a Kahn – Kahnfahrschule & Verleih', desc=META[s]['desc'], body=body, og='fliess-2'))

    # ---------------------------------------------------------------- Hofführung
    s = 'hoffuehrung'
    body = phero(blk(s, 0), blk(s, 1), 'Erleben · Hofführung', img('fuehrung-stall', 'Besucher am Futtertrog im Stall', '(max-width:860px) 70vw, 30vw', eager=True, widths=[426]),
                 crumbs=[('Erleben', '/kahnfahrten/')], ratio='ar-34', actions=btn('Hofführung anfragen', '/kontakt/') + btn('Online buchen', SITE['checkfront'], 'ghost', extra=' rel="noopener"'))
    body += section(f'''
<div class="split split--top">
  <div class="prose">{reveal(paras(s, 2, 4))}
    {reveal('<div class="note">' + ICON['info'] + '<p>Den Rundgang über den Mutschenhof können Sie auch zu einer Kahnfahrt dazubuchen (5,00&nbsp;€ pro Person). Die Online-Buchung läuft über das externe Buchungssystem Checkfront.</p></div>')}
    {reveal(f'<div class="btn-row">{btn("Hofführung anfragen", "/kontakt/")}{btn("Zu den Kahnfahrten", "/kahnfahrten/", "ghost")}</div>')}</div>
  <div class="reveal" style="--d:.1s">{gallery([('fuehrung-hof', 'Gäste auf dem gepflasterten Hof vor der Scheune', 'Auf dem Hof'), ('fuehrung-schweine', 'Kinder füttern Schweine', 'Artgerechte Tierhaltung'), ('fuehrung-stall', 'Besucher am Futtertrog', 'Hautnah erleben')], 'fuehrung', even=True)}</div>
</div>''')
    body += more([('/artgerechte-tierhaltung/', 'Der Hof', 'Artgerechte Tierhaltung', 'Rinder, Schweine und Hühner.'),
                  ('/hofeigene-schlachtung/', 'Schlachterei', 'Hofeigene Spezialitäten', 'Zum Abschluss eine kleine Verkostung.'),
                  ('/kahnfahrten/', 'Erleben', 'Kahnfahrten', 'Individuell gestaltbar, ab zwei Personen.')])
    pages.append(dict(slug=s, title='Hofführungen', desc=META[s]['desc'], body=body, og='fuehrung-hof'))

    # ---------------------------------------------------------------- Tipps für den Aufenthalt
    s = 'tipps-fuer-den-aufenthalt'
    def tcard(title, items, imgs, link=None):
        li = ''.join(f'<li>{i}</li>' for i in items)
        ims = ''.join(f'<div class="pic ar-32">{img(k, a, "(max-width:900px) 90vw, 30vw", widths=[360, 640])}</div>' for k, a in imgs)
        l = f'<p style="margin-top:1rem"><a class="link-arrow" href="{link}" rel="noopener">Zur Website{ICON["arrow"]}</a></p>' if link else ''
        return f'<article class="card reveal"><div class="stack" style="margin-bottom:1.4rem">{ims}</div><h3>{title}</h3><ul class="checks">{li}</ul>{l}</article>'
    body = phero('Der Spreewald', blk(s, 1), 'Tipps für den Aufenthalt', img('lehde', 'Blick über das Fließ auf ein Haus mit rotem Dach in Lehde', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 640], pos='55% 50%'),
                 crumbs=[('Besuch', '/tipps-fuer-den-aufenthalt/')], ratio='ar-43')
    body += section(f'<div class="prose" style="max-width:46rem;margin-inline:auto">{reveal(paras(s, 2, 4))}</div>', narrow=True, cls='section--tight')
    body += section(f'''<div class="head center">{eyebrow('Erkunden Sie die Umgebung')}<h2>{blk(s, 4)}</h2></div>
<div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr))">
 {tcard(plain(blk(s, 5)), blks(s, 6, 9), [('luebbenau-ortskern', 'Historischer Ortskern von Lübbenau'), ('spreewaldhafen', 'Großer Spreewaldhafen')])}
 {tcard(plain(blk(s, 9)), blks(s, 10, 13), [('lehde', 'Lehde im Spreewald'), ('kahn-lehde', 'Kahnfahrt im Spreewald')])}
 {tcard('In der Umgebung', blks(s, 13, 17), [('branitz', 'Schloss Branitz'), ('spreewelten', 'Spreewelten Lübbenau')], link='https://www.spreewelten.de')}
</div>''', cls='section--alt', wave_top='--cream-2')
    body += more([('/kahnfahrten/', 'Erleben', 'Kahnfahrt ab Mutschenhof', 'Von hier beginnen unsere Kahnfahrten durch Fließe, Wiesen und uralte Bäume.'),
                  ('/rent-a-kahn/', 'Erleben', 'Rent a Kahn', 'Selbst staken – wir weisen Sie ein.'),
                  ('/wegbeschreibung/', 'Besuch', 'Anfahrt', 'Wir sehen uns am Kahn!')])
    pages.append(dict(slug=s, title='Tipps für den Aufenthalt im Spreewald', desc=META[s]['desc'], body=body, og='lehde'))
    return pages
