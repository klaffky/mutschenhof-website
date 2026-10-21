"""Bausteine für die Mutschenhof-Website: Konfiguration, Bildverarbeitung, Layout, Komponenten."""
import hashlib, html, json, re, shutil
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'site'
DIST = ROOT / 'dist'
IMG_SRC = SRC / 'assets' / 'img-src'

# ---------------------------------------------------------------- Konfiguration
SITE = dict(
    name='Mutschenhof',
    url='https://mutschenhof-spreewald.de',          # für Sitemap/Canonical – bei Bedarf anpassen
    tel='0151 55 322 032', tel_href='+4915155322032',
    mail='info@mutschenhof.de',
    street='Kaupen 9b', zip='03222', city='Lübbenau', district='Ortsteil Lehde',
    facebook='https://www.facebook.com/mutschenhof',
    instagram='https://www.instagram.com/mutschenhof_spreewald/',
    maps_hof='https://goo.gl/maps/U13pxTtcYBU587b4A',
    maps_anfahrt='https://goo.gl/maps/xp45B6UoZYu87sJJA',
    checkfront='https://localtour.checkfront.com/reserve/?item_id=758',
)
CONTENT = json.loads((SRC / 'content.json').read_text(encoding='utf8'))
META = json.loads((SRC / 'meta-original.json').read_text(encoding='utf8'))
DATES = json.loads((SRC / 'data' / 'schlachttermine.json').read_text(encoding='utf8'))

NAV = [
    ('Der Hof', [('/der-mutschenhof/', 'Der Mutschenhof'), ('/oekologische-landwirtschaft/', 'Ökologische Landwirtschaft'),
                 ('/artgerechte-tierhaltung/', 'Artgerechte Tierhaltung'), ('/freiwilliges-oekologisches-jahr-foej/', 'Freiwilliges ökologisches Jahr')]),
    ('/ferienwohnungen/', 'Ferienwohnungen'),
    ('Erleben', [('/kahnfahrten/', 'Kahnfahrten'), ('/rent-a-kahn/', 'Rent a Kahn'), ('/hoffuehrung/', 'Hofführungen'),
                 ('/tipps-fuer-den-aufenthalt/', 'Der Spreewald & Ausflugstipps')]),
    ('/hofeigene-schlachtung/', 'Schlachterei'),
    ('Besuch', [('/wegbeschreibung/', 'Anfahrt'), ('/buchungskalendar/', 'Buchungskalender'), ('/kontakt/', 'Kontakt')]),
]

# ---------------------------------------------------------------- Texte aus der alten Seite
def blk(slug, i):
    return CONTENT[slug][i]['x']

def blks(slug, a, b=None):
    return [x['x'] for x in CONTENT[slug][a:b]]

def strip_head(x):
    """Entfernt eine führende Fett-Überschrift (<strong>…</strong><br>) aus einem Absatz."""
    return re.sub(r'^<strong>.*?</strong>(<br>)*', '', x).strip()

def paras(slug, a, b=None):
    return '\n'.join(f'<p>{p}</p>' for p in blks(slug, a, b))

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- Bilder
_meta, _needed = {}, {}
WIDTHS = [360, 640, 960, 1280, 1600, 1920]

def _info(key):
    if key not in _meta:
        f = next(IMG_SRC.glob(key + '.*'))
        with Image.open(f) as im:
            _meta[key] = (f, im.width, im.height)
    return _meta[key]

def _widths(key, widths=None, up=None):
    _, w, _ = _info(key)
    ws = [x for x in (widths or WIDTHS) if x < w]
    ws.append(min(w, max(widths or WIDTHS)))
    if up is None: up = not key.startswith(('logo', 'badge'))
    if up and w < 1100:            # kleine Originale: 2x sauber hochgerechnet, damit Retina-Handys nicht selbst (weich) skalieren
        ws.append(w * 2)
    return sorted(set(ws))

def _url(key, w):
    _needed[(key, w)] = True
    return f'/img/{key}-{w}.webp'

def img(key, alt, sizes='100vw', cls='', eager=False, widths=None, pos=None, extra=''):
    f, w, h = _info(key)
    ws = _widths(key, widths)
    srcset = ', '.join(f'{_url(key, x)} {x}w' for x in ws)
    big = ws[-1]
    style = f' style="object-position:{pos}"' if pos else ''
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="{_url(key, ws[min(len(ws)-1, 2)])}" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" '
            f'width="{big}" height="{round(big*h/w)}" loading="{load}" decoding="async"{c}{style} {extra}>').replace(' >', '>')

def pic(key, alt, ratio='ar-32', sizes='100vw', cls='', **kw):
    return f'<div class="pic {ratio} {cls}">{img(key, alt, sizes, **kw)}</div>'

def full(key, w=1600):
    ws = _widths(key, [x for x in WIDTHS if x <= w] or [w], up=True)
    return _url(key, ws[-1])

def write_images():
    out = DIST / 'img'
    out.mkdir(parents=True, exist_ok=True)
    cache = {}
    for (key, w) in sorted(_needed):
        dst = out / f'{key}-{w}.webp'
        f, sw, sh = _info(key)
        if key not in cache:
            cache[key] = Image.open(f)
            cache[key].load()
        im = cache[key]
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        if w != im.width:
            im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
            if w > sw:   # hochgerechnet: Kanten leicht nachschärfen
                im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))
            elif w < sw:
                im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=30, threshold=2))
        q = 88 if (w > sw or sw <= 640) else 82
        im.save(dst, 'WEBP', quality=q, method=6)
    return len(_needed)

# ---------------------------------------------------------------- Icons
ICON = {
    'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'chev': '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>',
    'fb': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.5-3.2h-3.2V7.7c0-.9.4-1.7 1.8-1.7h1.5V3.2S15.5 3 14.3 3C11.8 3 10.2 4.5 10.2 7.2v2.6H7.5V13h2.7v8z"/></svg>',
    'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>',
    'info': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.6v.1"/></svg>',
}

def btn(text, href, kind='', arrow=True, extra=''):
    k = f' btn--{kind}' if kind else ''
    ic = ICON['arrow'] if arrow else ''
    return f'<a class="btn{k}" href="{href}"{extra}>{text}{ic}</a>'

def link_arrow(text, href):
    return f'<a class="link-arrow" href="{href}">{text}{ICON["arrow"]}</a>'

def eyebrow(t):
    return f'<p class="eyebrow">{t}</p>'

def reveal(inner, tag='div', cls='', delay=0):
    d = f' style="--d:{delay}s"' if delay else ''
    return f'<{tag} class="reveal {cls}"{d}>{inner}</{tag}>'

def wave(color_var='--cream', flip=False, where='top'):
    t = ' style="transform:scaleY(-1)"' if flip else ''
    return (f'<svg class="wave wave--{where}" viewBox="0 0 1440 64" preserveAspectRatio="none" aria-hidden="true"{t} '
            f'style="color:var({color_var})"><path d="M0 34C140 62 300 6 520 30s420 36 640 8 220-24 280-8v34H0z"/></svg>')

def gallery(items, group, even=False, cols=None):
    """items: [(key, alt, caption)] – öffnet die Lightbox."""
    a = ''
    for key, alt, cap in items:
        nat = _info(key)[1]
        nat = f' data-native="{nat}"' if nat < 1100 else ''   # kleine Originale in der Lightbox nicht über ~1,35x aufziehen
        a += (f'<a class="lb" href="{full(key, 1600)}"{nat} data-group="{group}" data-alt="{esc(alt)}" data-caption="{esc(cap)}">'
              f'{img(key, alt, "(max-width:700px) 50vw, 25vw", widths=[360, 640, 960])}</a>')
    return f'<div class="gallery{" gallery--even" if even else ""}{" gallery--3" if cols == 3 else ""}">{a}</div>'

def embed(src, title, kind, bg_key=None, video=False, tall=False, light=False, text=''):
    cls = 'embed' + (' embed--video' if video else '') + (' embed--tall' if tall else '') + (' embed--light' if light else '')
    bg = f'<div class="embed-bg" aria-hidden="true">{img(bg_key, "", "100vw", widths=[640, 960])}</div>' if bg_key else ''
    v = ' data-video' if video else ''
    return (f'<div class="{cls}" data-src="{esc(src)}" data-title="{esc(title)}"{v}>{bg}'
            f'<div class="embed-inner"><h3>{title}</h3><p>{text}</p>'
            f'<button type="button" class="btn embed-load{" btn--light" if not light else ""}">{kind}{ICON["arrow"]}</button></div></div>')

# ---------------------------------------------------------------- Seitenkopf (Unterseiten)
FLIESS = ('<svg class="phero-fliess" viewBox="0 0 700 500" aria-hidden="true"><path d="M20 40C180 10 220 160 380 130s160-140 300-90"/>'
          '<path d="M0 120C170 90 210 250 380 215s180-150 320-100"/><path d="M60 330C200 300 260 420 420 380s200-110 280-60"/>'
          '<path d="M300 130c20 90-20 150 40 250"/></svg>')

def phero(h1, lede='', eyebrow_text='', media='', crumbs=(), actions='', ratio='ar-45'):
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Brotkrumen"><a href="/">Start</a>' + ''.join(
            f'<span>/</span><a href="{u}">{t}</a>' for t, u in crumbs) + '</nav>'
    ey = eyebrow(eyebrow_text) if eyebrow_text else ''
    lead = f'<p class="lede">{lede}</p>' if lede else ''
    act = f'<div class="btn-row">{actions}</div>' if actions else ''
    m = f'<div class="phero-media reveal"><div class="frame arch"><div class="pic {ratio}">{media}</div></div></div>' if media else ''
    return (f'<header class="phero grain">{FLIESS}<div class="container phero-grid"><div>{cr}{ey}<h1>{h1}</h1>{lead}{act}</div>{m}</div></header>')

def section(inner, cls='', id='', narrow=False, wave_top=None):
    i = f' id="{id}"' if id else ''
    w = wave(wave_top) if wave_top else ''
    c = 'container container--narrow' if narrow else 'container'
    return f'<section class="section {cls}"{i}>{w}<div class="{c}">{inner}</div></section>'

# ---------------------------------------------------------------- Layout
def _nav_html(path):
    out = []
    for item in NAV:
        if isinstance(item[1], list):
            label, subs = item
            cur = any(u == path for u, _ in subs)
            sid = 'sub-' + re.sub(r'\W', '', label.lower())
            lis = ''.join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == path else ""}>{t}</a></li>' for u, t in subs)
            out.append(f'<li class="has-sub{" is-current" if cur else ""}"><button type="button" class="nav-link" aria-expanded="false" aria-controls="{sid}">{label}{ICON["chev"]}</button><ul class="sub" id="{sid}">{lis}</ul></li>')
        else:
            u, t = item
            out.append(f'<li><a class="nav-link" href="{u}"{" aria-current=\"page\"" if u == path else ""}>{t}</a></li>')
    return '<ul>' + ''.join(out) + '</ul>'

def header(path, has_hero):
    return f'''<header class="site-header{'' if has_hero else ' is-solid'}">
  <div class="header-inner">
    <a class="brand" href="/" aria-label="Mutschenhof – zur Startseite">
      {img('logo-hell', '', '46px', cls='logo-light', eager=True, widths=[96, 192]).replace('alt=""', 'alt="" aria-hidden="true"')}
      {img('logo', '', '46px', cls='logo-dark', eager=True, widths=[96, 192]).replace('alt=""', 'alt="" aria-hidden="true"')}
      <span class="brand-text"><span class="brand-name">Mutschenhof</span><span class="brand-sub">Lehde · Spreewald</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Hauptnavigation">
      {_nav_html(path)}
      <a class="btn nav-cta-mobile btn--light" href="/buchungskalendar/">Online buchen{ICON['arrow']}</a>
    </nav>
    <a class="btn header-cta" href="/buchungskalendar/">Online buchen{ICON['arrow']}</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
  </div>
</header>'''

def footer():
    S = SITE
    return f'''<footer class="site-footer">
  <svg class="footer-wave" viewBox="0 0 1440 64" preserveAspectRatio="none" aria-hidden="true"><path d="M0 34C140 62 300 6 520 30s420 36 640 8 220-24 280-8v34H0z" transform="translate(0 64) scale(1 -1)"/></svg>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        {img('logo-hell', 'Mutschenhof Spreewald – Logo', '120px', widths=[120, 240])}
        <p>Ein Hof mit besonderer Note für Naturliebhaber, Wasserfreunde und Entdecker.</p>
        <div class="social">
          <a href="{S['facebook']}" rel="noopener" aria-label="Mutschenhof auf Facebook">{ICON['fb']}</a>
          <a href="{S['instagram']}" rel="noopener" aria-label="Mutschenhof auf Instagram">{ICON['ig']}</a>
        </div>
      </div>
      <div>
        <h2>Kontakt</h2>
        <address class="address">Mutschenhof UG<br>Anja Kilka<br>{S['street']}<br>{S['zip']} {S['city']}<br>{S['district']}</address>
        <ul style="margin-top:1rem"><li><a href="tel:{S['tel_href']}">{S['tel']}</a></li><li><a href="mailto:{S['mail']}">{S['mail']}</a></li></ul>
      </div>
      <div>
        <h2>Auf dem Hof</h2>
        <ul>
          <li><a href="/ferienwohnungen/">Ferienwohnungen</a></li><li><a href="/kahnfahrten/">Kahnfahrten</a></li>
          <li><a href="/rent-a-kahn/">Rent a Kahn</a></li><li><a href="/hoffuehrung/">Hofführungen</a></li>
          <li><a href="/hofeigene-schlachtung/">Schlachterei</a></li><li><a href="/freiwilliges-oekologisches-jahr-foej/">FÖJ</a></li>
        </ul>
      </div>
      <div>
        <h2>Besuch</h2>
        <ul>
          <li><a href="/wegbeschreibung/">Anfahrt</a></li><li><a href="/buchungskalendar/">Buchungskalender</a></li>
          <li><a href="/tipps-fuer-den-aufenthalt/">Tipps für den Aufenthalt</a></li><li><a href="/kontakt/">Kontakt</a></li>
        </ul>
        <div class="badge">{img('badge-referenzbetrieb', 'Referenzbetrieb Biosphärenreservat Spreewald', '56px', widths=[112])}<span>Referenzbetrieb<br>Biosphärenreservat Spreewald</span></div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Mutschenhof UG · Lehde im Spreewald</span>
      <ul><li><a href="/impressum/">Impressum</a></li><li><a href="/datenschutz/">Datenschutz</a></li></ul>
    </div>
  </div>
</footer>'''

_asset_cache = {}
def _asset(rel):
    """Kopiert Asset mit Hash im Dateinamen (Cache-Busting) und liefert die URL."""
    if rel in _asset_cache:
        return _asset_cache[rel]
    src = SRC / 'assets' / rel
    h = hashlib.md5(src.read_bytes()).hexdigest()[:8]
    name = f'{src.stem}.{h}{src.suffix}'
    dst = DIST / 'assets' / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    dst.write_bytes(data)
    _asset_cache[rel] = f'/assets/{name}'
    return _asset_cache[rel]

def render(p):
    """p: dict(slug,title,desc,body,hero,theme,og,jsonld,noindex)"""
    slug = p['slug']
    path = '/' if slug == '' else f'/{slug}/'
    has_hero = p.get('hero', False)
    title = p['title'] if slug == '' else f"{p['title']} – Mutschenhof im Spreewald"
    desc = esc(p.get('desc') or '')
    canon = SITE['url'] + path
    og = SITE['url'] + full(p['og'], 1280) if p.get('og') else ''
    css, js = _asset('css/main.css'), _asset('js/main.js')
    theme = f' theme-{p["theme"]}' if p.get('theme') else ''
    ld = f'<script type="application/ld+json">{json.dumps(p["jsonld"], ensure_ascii=False)}</script>' if p.get('jsonld') else ''
    robots = '<meta name="robots" content="noindex">' if p.get('noindex') else ''
    ogtags = (f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{desc}">'
              f'<meta property="og:type" content="website"><meta property="og:locale" content="de_DE">'
              f'<meta property="og:url" content="{canon}">' + (f'<meta property="og:image" content="{og}">' if og else ''))
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#17291e">
{robots}<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
{ogtags}
<link rel="preload" href="/assets/fonts/lora-var.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/fonts/inter-regular.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{css}">
{ld}
</head>
<body class="{'' if has_hero else 'no-hero'}{theme}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{header(path, has_hero)}
<main id="inhalt">
{p['body']}
</main>
{footer()}
<script src="{js}" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- Schlachttermine
def _de(iso):
    y, m, d = iso.split('-')
    return f'{d}.{m}.{y}'

def countdown():
    """Zeigt den nächsten Termin aus site/data/schlachttermine.json; sonst einen neutralen Hinweis."""
    dates = json.dumps(DATES['termine'])
    fb = ' · '.join(_de(x) for x in DATES['termine'])
    cells = ''.join(f'<div><b data-u="{u}">0</b><span>{t}</span></div>'
                    for u, t in (('d', 'Tage'), ('h', 'Std.'), ('m', 'Min.'), ('s', 'Sek.')))
    return (f"<div class=\"cd\" data-dates='{dates}'>"
            f'<div class="cd-yes" hidden><p class="eyebrow">Nächster Schlachttermin</p><p class="next-date"></p>'
            f'<div class="countdown" role="timer" aria-label="Countdown bis zum nächsten Schlachttermin">{cells}</div></div>'
            f'<div class="cd-no" hidden><p class="eyebrow">Schlachttermine</p>'
            f'<p class="next-date">Neue Termine folgen.</p>'
            f'<p>Die Termine der Saison {DATES["saison"]} sind vorbei. Neue Termine werden hier ergänzt.</p></div>'
            f'<p class="cd-fallback">Schlachttermine Saison {DATES["saison"]}: {fb}</p></div>')


def more(items, title='Weiterlesen'):
    """Querverweis-Karten am Seitenende: [(href, kicker, titel, text)]"""
    cards = ''.join(f'<a class="card reveal" href="{h}" style="text-decoration:none;display:block">{eyebrow(k)}<h3>{t}</h3><p>{x}</p>'
                    f'<span class="link-arrow">Ansehen{ICON["arrow"]}</span></a>' for h, k, t, x in items)
    return section(f'<div class="head center">{eyebrow(title)}</div><div class="cards">{cards}</div>', cls='section--alt', wave_top='--cream-2')

def rows(items):
    """Wechselnde Text/Bild-Zeilen: [(h2, html, bildhtml)]"""
    out = ''
    for i, (h, body, media) in enumerate(items):
        rev = ' split--reverse' if i % 2 else ''
        out += (f'<div class="split split--top{rev}" style="margin-bottom:clamp(3rem,6vw,5.5rem)"><div class="prose">'
                f'{reveal("<h2>" + h + "</h2>")}{reveal(body)}</div><div class="reveal" style="--d:.1s">{media}</div></div>')
    return out


# ---------------------------------------------------------------- Formulare (E-Mail-Versand per mailto)
def f_text(name, label, type_='text', req=False, extra='', hint=''):
    r = ' required' if req else ''
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    h = f'<small>{hint}</small>' if hint else ''
    return (f'<div class="field"><label for="f-{name}">{label}{star}</label>'
            f'<input id="f-{name}" name="{name}" data-label="{esc(label)}" type="{type_}"{r} {extra}>{h}</div>')

def f_select(name, label, options, req=False, placeholder='bitte auswählen'):
    r = ' required' if req else ''
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    opts = f'<option value="">{placeholder}</option>' + ''.join(f'<option>{o}</option>' for o in options)
    return f'<div class="field"><label for="f-{name}">{label}{star}</label><select id="f-{name}" name="{name}" data-label="{esc(label)}"{r}>{opts}</select></div>'

def f_choice(name, label, options, kind='radio', req=False):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    items = ''
    for i, o in enumerate(options):
        r = ' required' if (req and kind == 'radio') else ''
        items += f'<label class="choice"><input type="{kind}" name="{name}" value="{esc(o)}" data-label="{esc(label)}"{r}><span>{o}</span></label>'
    return f'<fieldset class="field"><legend>{label}{star}</legend><div class="choices">{items}</div></fieldset>'

def f_stepper(name, label, val=0, mn=0, mx=99, hint=''):
    h = f'<small>{hint}</small>' if hint else ''
    return (f'<div class="field"><label for="f-{name}">{label}</label><div class="stepper">'
            f'<button type="button" data-step="-1" aria-label="weniger">−</button>'
            f'<input id="f-{name}" name="{name}" data-label="{esc(label)}" type="number" min="{mn}" max="{mx}" value="{val}" inputmode="numeric">'
            f'<button type="button" data-step="1" aria-label="mehr">+</button></div>{h}</div>')

def f_area(name, label, req=False):
    r = ' required' if req else ''
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    return f'<div class="field"><label for="f-{name}">{label}{star}</label><textarea id="f-{name}" name="{name}" data-label="{esc(label)}"{r}></textarea></div>'

def f_consent():
    return ('<label class="check"><input type="checkbox" name="dsgvo" required><span>Ich habe die <a class="link" href="/datenschutz/">Datenschutzerklärung</a> gelesen '
            'und bin damit einverstanden, dass meine Angaben per E-Mail an den Mutschenhof übermittelt werden, damit meine Anfrage beantwortet werden kann. '
            '<span class="req" aria-hidden="true">*</span></span></label>')

def form(subject, inner, submit='Anfrage senden'):
    return (f'<form class="form" data-mailto="{SITE["mail"]}" data-subject="{esc(subject)}">{inner}{f_consent()}'
            f'<div><button class="btn" type="submit">{submit}{ICON["arrow"]}</button></div>'
            f'<div class="form-status" role="status" hidden></div>'
            f'<p class="caption">Mit „{submit}“ öffnet sich Ihr E-Mail-Programm mit der vorbereiteten Nachricht. Felder mit <span class="req">*</span> sind Pflichtfelder.</p></form>')
