import re
from lib import *

def legal_page(slug, title, extra=''):
    out = ''
    for i, b in enumerate(CONTENT[slug]):
        if i == 0:
            continue
        t, x = b['t'], b['x']
        if t == 'li':
            continue
        if t == 'h4' or (t == 'p' and re.fullmatch(r'<strong>[^<]*</strong>', x)):
            out += f'<h3>{re.sub("<[^>]+>", "", x)}</h3>'
        else:
            out += f'<p>{x}</p>'
    return out

def datenschutz():
    s = 'datenschutz'
    B = [b['x'] for b in CONTENT[s]]
    items = ['Datum und Uhrzeit der Anforderung', 'Name der angeforderten Datei', 'Seite, von der aus die Datei angefordert wurde', 'Zugriffsstatus',
             'Verwendeter Webbrowser und verwendetes Betriebssystem', '(Vollständige) IP-Adresse des anfordernden Rechners', 'Übertragene Datenmenge']
    # Im Originaltext ist die Aufzählung mitten in den Kontaktformular-Absatz gerutscht – hier an ihren Platz gesetzt.
    b10 = B[10].replace('<br>', ' ')
    for it in items:
        b10 = b10.replace(it + ' ', '', 1)
    b10 = re.sub(r'\s+', ' ', b10).replace('sowie ggf. Art.', 'sowie ggf. Art.')
    b8 = B[8].replace('<br>', ' ')
    b8 = b8.replace('aufgezeichnet: ', 'aufgezeichnet:</p><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul><p>')
    b20 = B[20].replace('<br>', ' ')
    parts = re.split(r' (?=Das Recht, |Recht auf Widerruf)', b20)
    b20 = '<p>' + parts[0] + '</p><ul>' + ''.join(f'<li>{p}</li>' for p in parts[1:]) + '</ul>'
    out = ''
    for i, x in enumerate(B[1:28], start=1):
        if i == 8: out += f'<p>{b8}</p>'
        elif i == 10: out += f'<p>{b10}</p>'
        elif i == 20: out += b20
        elif i == 4: out += f'<p>{x}</p>'
        elif re.fullmatch(r'<strong>[^<]*</strong>', x): out += f'<h3>{re.sub("<[^>]+>", "", x)}</h3>'
        else: out += f'<p>{x.replace("<br>", " ")}</p>'
    out += ('<h3>Externe Inhalte, die Sie selbst laden</h3>'
            '<p>Auf einigen Seiten können Sie per Klick externe Inhalte laden: ein Video von YouTube (youtube-nocookie.com, Google), die Belegungskalender und das Anfrageformular '
            'von fungiwo.de sowie – über einen Link – das Buchungssystem Checkfront. Erst nach Ihrem Klick werden diese Inhalte geladen; dabei werden Daten, z. B. Ihre IP-Adresse, '
            'an den jeweiligen Anbieter übertragen.</p>')
    return out

def build():
    pages = []
    # ---------------------------------------------------------------- Anfahrt
    s = 'wegbeschreibung'
    steps = ''.join(f'<li><p>{blk(s, i)}</p></li>' for i in range(2, 6))
    body = phero(blk(s, 0), blk(s, 1), 'Anfahrt', img('kahn-hof', 'Kahn vor dem Haus am Fließ', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 540], pos='50% 55%'),
                 crumbs=[('Besuch', '/wegbeschreibung/')], ratio='ar-43',
                 actions=btn('In Google Maps öffnen', SITE['maps_anfahrt'], extra=' rel="noopener"') + btn('Wir rufen an: ' + SITE['tel'], 'tel:' + SITE['tel_href'], 'ghost', arrow=False))
    body += section(f'''
<div class="split split--top">
  <div>{reveal('<ol class="steps">' + steps + '</ol>')}
    {reveal('<p style="font:500 clamp(1.6rem,2vw + 1rem,2.4rem)/1.2 var(--font-head);margin-top:2.5rem">' + blk(s, 6) + '</p>')}</div>
  <div class="reveal" style="--d:.1s"><a class="lb" href="{full('anfahrt-karte')}" data-group="karte" data-alt="Anfahrtsskizze: von Lübbenau kommend nach Lehde" data-caption="Anfahrtsskizze" style="display:block;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)">{img('anfahrt-karte', 'Anfahrtsskizze: von Lübbenau kommend nach Lehde, nach der scharfen Rechtskurve die steile Brücke und dann der Parkplatz', '(max-width:860px) 92vw, 46vw', widths=[480, 589])}</a>
  <p class="caption">Anfahrtsskizze – zum Vergrößern anklicken.</p></div>
</div>''')
    pages.append(dict(slug=s, title='Wegbeschreibung / Anfahrt', desc=META[s]['desc'], body=body, og='kahn-hof'))

    # ---------------------------------------------------------------- Kontakt
    s = 'kontakt'
    wa = 'https://wa.me/' + SITE['tel_href'].lstrip('+')
    fm = form('Anfrage über die Website', '<div class="row">' + f_select('anrede', 'Anrede', ['Herr', 'Frau', 'Divers', 'Familie', 'Gruppe']) + f_text('name', 'Name', req=True, extra='autocomplete="name"') + '</div>'
              '<div class="row">' + f_text('email', 'E-Mail', 'email', True, 'autocomplete="email"') + f_text('tel', 'Telefonnummer', 'tel', True, 'autocomplete="tel"') + '</div>'
              + f_area('nachricht', 'Ihre Nachricht', True), 'Nachricht senden')
    body = phero('Kontakt', 'Schreiben Sie uns oder rufen Sie an – wir freuen uns auf Sie.', 'Mutschenhof', img('kahn-staker', 'Kahn mit Stakerin auf einem Fließ', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 540], pos='45% 50%'),
                 crumbs=[('Besuch', '/kontakt/')], ratio='ar-43')
    body += section(f'''
<div class="split split--wide-media split--top">
  <div class="card reveal">
    <h2 style="font-size:1.6rem">So erreichen Sie uns</h2>
    <address class="address"><b>Mutschenhof UG</b><br>Anja Kilka<br><br><b>Mutschenhof</b><br>Sebastian Kilka<br><br>{SITE['street']}<br>{SITE['zip']} {SITE['city']}<br>{SITE['district']}</address>
    <ul class="stack" style="list-style:none;margin:1.4rem 0">
      <li>Telefon: <a class="link" href="tel:{SITE['tel_href']}">{SITE['tel']}</a></li>
      <li>E-Mail: <a class="link" href="mailto:{SITE['mail']}">{SITE['mail']}</a></li>
      <li><a class="link" href="{wa}" rel="noopener">Per WhatsApp schreiben</a></li>
      <li><a class="link" href="{SITE['facebook']}" rel="noopener">Facebook</a> · <a class="link" href="{SITE['instagram']}" rel="noopener">Instagram</a></li>
    </ul>
    {link_arrow('Zur Wegbeschreibung', '/wegbeschreibung/')}
  </div>
  <div class="card reveal" style="--d:.1s">{fm}</div>
</div>''')
    pages.append(dict(slug=s, title='Kontakt', desc='Kontakt zum Mutschenhof in Lehde im Spreewald: Telefon, E-Mail, Adresse und Kontaktformular.', body=body, og='kahn-staker'))

    # ---------------------------------------------------------------- Impressum / Datenschutz
    body = f'<div class="no-hero-pad"></div>' + section(f'<div class="legal"><h1 style="font-size:clamp(2.2rem,3vw + 1rem,3.4rem)">Impressum</h1>{legal_page("impressum", "Impressum")}</div>', narrow=True, cls='section--tight')
    pages.append(dict(slug='impressum', title='Impressum', desc='Impressum des Mutschenhofs in Lehde, Spreewald.', body=body))
    body = section(f'<div class="legal"><h1 style="font-size:clamp(2.2rem,3vw + 1rem,3.4rem)">Datenschutzerklärung</h1>{datenschutz()}</div>', narrow=True, cls='section--tight')
    pages.append(dict(slug='datenschutz', title='Datenschutz', desc='Datenschutzerklärung des Mutschenhofs in Lehde, Spreewald.', body=body))

    # ---------------------------------------------------------------- 404
    body = section(f'<div class="center">{eyebrow("Fehler 404")}<h1>Hier ist nur Wasser.</h1><p class="lede">Diese Seite gibt es nicht (mehr). Vielleicht hilft Ihnen einer dieser Wege weiter.</p><div class="btn-row" style="justify-content:center">{btn("Zur Startseite", "/")}{btn("Ferienwohnungen", "/ferienwohnungen/", "ghost")}{btn("Kontakt", "/kontakt/", "ghost")}</div></div>', narrow=True)
    pages.append(dict(slug='404', title='Seite nicht gefunden', desc='', body=body, noindex=True))
    return pages
