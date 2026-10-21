from lib import *

HERO_WAVE = ('<svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M0 48C150 88 330 6 560 38s470 46 690 6c80-14 150-22 190-14v60H0z"/></svg>')

def tile(href, kicker, title, text, key, alt, pos=None, extra=''):
    return (f'<a class="tile reveal {extra}" href="{href}"><div class="pic">{img(key, alt, "(max-width:620px) 100vw, (max-width:980px) 50vw, 33vw", widths=[480, 800, 1200], pos=pos)}</div>'
            f'<span class="go">{ICON["arrow"]}</span>'
            f'<div class="tile-body"><span class="kicker">{kicker}</span><h3>{title}</h3><p>{text}</p></div></a>')

YEAR = [
    ('Ende März bis Anfang April', 'Der Winterstau wird abgesenkt',
     'Im Staubereich Lehde sinkt das Wasser. Je nach Wetterlage geht es ab Ende April auf die Ackerflächen – alle Geräte reisen mit dem Kahn.'),
    ('Frühling bis Herbst', 'Die Mutschen auf den Spreewaldwiesen',
     'Die Rinderherde beweidet die Wiesen. Nur im Frühling darf der größte Bulle die Damen beglücken – und schenkt uns Nachwuchs.'),
    ('Anfang Juni', 'Heuernte – die Zeit steht still',
     'Mähen und Pressen bestimmen die Tage. Mit einer Fuhre fahren bis zu 7 Heuballen im Kahn auf die Insel.'),
    ('Zur Erntezeit', 'Kürbisse, Kartoffeln und Getreide',
     'Auch die Ernte reist per Kahn. Wenn er randvoll mit Kartoffeln über die Spree fährt, gibt es erstaunte Blicke von den Touristen.'),
    ('November', 'Der Winterstau kommt',
     'Die Spree wird angestaut, die Wiesen stehen unter Wasser. Die Rinder fahren in Dreiergruppen mit dem Kahn zum Hof auf die Koppel.'),
    ('Wenn die Fließe zufrieren', 'Die Arbeit wartet',
     'Ohne Kahn kommt niemand auf die Flächen. Dann ruht alles, bis die Fließe wieder frei sind.'),
]

def build():
    h = 'der-mutschenhof'
    hero = f'''<section class="hero" aria-labelledby="h1">
  <div class="hero-media">{img('hero-kahn-rinder', 'Ein Kahn gleitet über ein Spreewaldfließ, am Ufer grasen Rinder', '100vw', eager=True, widths=[640, 960, 1280, 1600, 1920])}</div>
  <div class="hero-inner">
    <p class="eyebrow">Lehde · Spreewald</p>
    <h1 id="h1">Mutschenhof</h1>
    <p class="hero-sub">Eine Insel im Spreewald, seit fünf Generationen in Familienhand – wo Mensch, Tier und Maschine noch mit dem Kahn reisen.</p>
    <div class="btn-row">{btn('Ferienwohnungen entdecken', '/ferienwohnungen/', 'light')}{btn('Kahnfahrt anfragen', '/kahnfahrten/', 'ghost-light')}</div>
  </div>
  <a class="scroll-cue" href="#willkommen">Entdecken</a>
  {HERO_WAVE}
</section>'''

    welcome = section(f'''
<div class="split split--wide-text">
  <div class="prose">
    {reveal(eyebrow('Willkommen'), 'div')}
    {reveal('<h2>Ein Hof mit besonderer Note</h2>')}
    {reveal('<p class="lede">Willkommen auf unserem familienbetriebenen Mutschenhof. Ein Hof mit besonderer Note für Naturliebhaber, Wasserfreunde und Entdecker.</p>')}
    {reveal(paras(h, 1, 3))}
    {reveal(link_arrow('Die Familie kennenlernen', '/der-mutschenhof/'))}
  </div>
  <div class="media-stack reveal" style="--d:.15s">
    <div class="frame arch"><div class="pic ar-45">{img('hof-kuerbisse', 'Kürbisse am Ufer, daneben ein Kahn am Steg des Mutschenhofs', '(max-width:860px) 90vw, 40vw', widths=[480, 800, 1200], pos='24% 50%')}</div></div>
    <div class="pic pic--float ar-43">{img('kahn-hund', 'Hund im Kahn, der über ein Spreewaldfließ gleitet', '25vw', widths=[360, 640], pos='70% 50%')}</div>
  </div>
</div>
<div class="facts reveal" style="margin-top:clamp(3.5rem,7vw,6rem)">
  <div class="fact"><b>5.</b><span>Generation der Familie Kilka auf dem Hof</span></div>
  <div class="fact"><b>1904</b><span>erbautes, denkmalgeschütztes Blockbohlenhaus</span></div>
  <div class="fact"><b>24</b><span>Rinder der Rasse Blonde d’Aquitaine – zurzeit</span></div>
  <div class="fact"><b>1991</b><span>erhielt das Biosphärenreservat Spreewald den Unesco-Status</span></div>
</div>''', id='willkommen')

    tiles = section(f'''
<div class="head center">{reveal(eyebrow('Auf dem Hof'))}{reveal('<h2>Wege auf unsere Insel</h2>')}</div>
<div class="tiles">
  {tile('/ferienwohnungen/', 'Ferienwohnungen', 'Wo man sich sofort zu Hause fühlt …', 'Unsere Traumferien-Wohnungen mitten im Spreewald.', 'lischka-terrasse', 'Terrasse vor dem Blockbohlenhaus mit Sitzgruppe')}
  {tile('/kahnfahrten/', 'Hof-Kahnfahrten', 'Romantischer geht es nicht', 'Individuell gestaltbar, ab zwei Personen buchbar.', 'kahn-hof', 'Kahn mit Gästen vor dem Haus am Fließ', pos='50% 60%')}
  {tile('/artgerechte-tierhaltung/', 'Artgerechte Tierhaltung', 'Wo Rinder ihre eigene Insel haben …', 'Rinder, Schweine, Hühner – und der Rest der Hofbande.', 'kuhweide', 'Rinder grasen am Wasser')}
  {tile('/oekologische-landwirtschaft/', 'Ökologische Landwirtschaft', 'Wo Tradition überall spürbar ist …', 'Zu Äckern und Wiesen geht es mit dem Kahn, wie vor hundert Jahren.', 'kahn-staker', 'Kahn mit Staker auf einem Fließ')}
  {tile('/hofeigene-schlachtung/', 'Schlachterei', 'Wo der Geschmack vom eigenen Hof kommt …', 'Spreewälder Rindfleisch aus der hofeigenen Schlachtung.', 'salami', 'Salami, Brot, Frischkäse und Käse auf einem Holzbrett', extra='tile--burgund')}
  {tile('/tipps-fuer-den-aufenthalt/', 'Der Spreewald', 'Wo Mythen und Sagen greifbar sind …', 'Ausflugstipps rund um Lehde und Lübbenau.', 'fliess-3', 'Ein stilles, grünes Spreewaldfließ')}
</div>''', cls='section--alt', wave_top='--cream-2')

    year = section(f'''
<div class="head center">{reveal(eyebrow('Der Hof im Jahreslauf'))}{reveal('<h2>Ein Jahr auf der Insel</h2>')}
{reveal('<p class="lede">„Kurz gesagt, unsere Arbeit richtet sich nach dem Spreewald.“</p>')}</div>
<ol class="year">
''' + ''.join(f'<li class="reveal"><div class="when"><b>{w}</b></div><div class="what"><strong>{t}</strong><p>{x}</p></div></li>' for w, t, x in YEAR) + f'''
</ol>
<p class="center" style="margin-top:2.5rem">{btn('Mehr zur ökologischen Landwirtschaft', '/oekologische-landwirtschaft/', 'light')}</p>''',
                   cls='section--dark', wave_top='--forest')

    kahn = section(f'''
<div class="split split--reverse">
  <div class="prose">
    {reveal(eyebrow('Kahnfahrten'))}{reveal('<h2>Unterwegs im Herzen des Spreewaldes</h2>')}
    {reveal('<p class="lede">Von hier aus beginnen unsere Kahnfahrten durch ein Labyrinth aus Fließen, Wiesen und uralten Bäumen.</p>')}
    {reveal('<p class="price"><b>ab 105&nbsp;€</b><span>pro Stunde · bereits ab zwei Personen buchbar</span></p>')}
    {reveal(f'<div class="btn-row" style="margin-top:0">{btn("Kahnfahrt anfragen", "/kahnfahrten/")}{btn("Selbst staken: Rent a Kahn", "/rent-a-kahn/", "ghost")}</div>')}
  </div>
  <div class="frame reveal" style="--d:.15s"><div class="pic ar-32 pic--shadow">{img('kahn-paar', 'Zwei Gäste im Kahn, hinter ihnen steht die Stakerin', '(max-width:860px) 92vw, 46vw', widths=[480, 800, 1200], pos='50% 40%')}</div></div>
</div>''')

    wohnen = section(f'''
<div class="split split--wide-media">
  <div class="media-stack reveal">
    <div class="pic ar-32 pic--shadow">{img('lischka-hof', 'Hof mit Sitzgruppe zwischen Blockhaus und Scheune', '(max-width:860px) 92vw, 50vw', widths=[360, 510])}</div>
    <div class="pic pic--float ar-43">{img('spreewa-kueche', 'Küche mit Holzwand und Blick in den Garten', '25vw', widths=[360, 510])}</div>
  </div>
  <div class="prose">
    {reveal(eyebrow('Ferienwohnungen'))}{reveal('<h2>Urlaub in einem alten Blockhaus</h2>')}
    {reveal('<p class="lede">In unserem 1904 erbauten, denkmalgeschützen Blockbohlenhaus stehen zwei liebevoll eingerichtete Ferienwohnungen für Sie bereit.</p>')}
    {reveal('<p>Durch die Holzwände, die Lehmdämmung und den traditionellen doppelten Holzfenstern bleiben die Zimmer in heißen Sommertagen angenehm kühl und in den kalten Herbst- und Wintermonaten schnell kuschlig warm.</p>')}
    {reveal(f'<div class="btn-row">{btn("Ferienwohnungen ansehen", "/ferienwohnungen/")}{btn("Online buchen", "/buchungskalendar/", "ghost")}</div>')}
  </div>
</div>''', cls='section--alt', wave_top='--cream-2')

    tiere = section(f'''
<div class="split split--wide-media">
  <div class="frame arch reveal"><div class="pic ar-45">{img('rinder-herbst', 'Zwei Rinder auf einer herbstlichen Weide unter Bäumen', '(max-width:860px) 88vw, 44vw', widths=[480, 800, 1200], pos='60% 50%')}</div></div>
  <figure class="quote reveal" style="--d:.1s">
    <blockquote>Unsere Tiere sind ein Teil des Hofes. Ohne all die Rinder, Schweine, Hühner, Katzen und unsere Hündin Wanda sowie Pfau Rex, wäre unsere Insel nicht das, was sie ist: ein Ort des Respekts, der Freude und der Verbundenheit.</blockquote>
    <figcaption class="cite"><cite>Familie Kilka</cite></figcaption>
    <div class="btn-row">{btn('Artgerechte Tierhaltung', '/artgerechte-tierhaltung/')}{btn('Hofführung erleben', '/hoffuehrung/', 'ghost')}</div>
  </figure>
</div>''')

    schlacht = f'''<section class="section section--accent theme-burgund" style="--accent:var(--burgund)">{wave('--burgund')}
<div class="container"><div class="split split--wide-text">
  <div>
    {reveal(eyebrow('Schlachterei'))}{reveal('<h2>Spreewälder Rindfleisch vom eigenen Hof</h2>')}
    {reveal('<p style="font:400 1.2rem/1.6 var(--font-head);max-width:36rem">Im Jahr 2022 wurde das hofeigene Schlachthaus in Betrieb genommen, wo regelmäßig qualitativ hochwertiges Fleisch von unseren Rindern der Rasse Blonde d’Aquitaine in Direkt-Vermarktung angeboten wird.</p>')}
    {reveal(f'<div class="btn-row">{btn("Zur Schlachterei", "/hofeigene-schlachtung/", "light")}</div>')}
  </div>
  <div class="reveal" style="--d:.1s">{countdown()}</div>
</div></div></section>'''

    foej_anfahrt = section(f'''
<div class="cards">
  <article class="card reveal">
    {eyebrow('Freiwilliges ökologisches Jahr')}
    <h3>Abwechslungsreiche, tier- und naturverbundene Arbeit?</h3>
    <p>Du möchtest Dich ausprobieren, neues Lernen und weg von der Schulbank? Dann bewirb Dich bei uns für ein freiwilliges ökologisches Jahr!</p>
    {link_arrow('Mehr zum FÖJ', '/freiwilliges-oekologisches-jahr-foej/')}
  </article>
  <article class="card reveal" style="--d:.1s">
    {eyebrow('Anfahrt')}
    <h3>Wir sehen uns am Kahn!</h3>
    <p>Vom Parkplatz in Lehde holen wir Sie mit dem Kahn ab. Geben Sie in Ihr Navi „Lehde Café Venedig“ ein.</p>
    {link_arrow('Wegbeschreibung', '/wegbeschreibung/')}
  </article>
  <article class="card reveal" style="--d:.2s">
    {eyebrow('Kontakt')}
    <h3>Mutschenhof UG</h3>
    <address class="address" style="margin-bottom:1rem">Kaupen 9b · 03222 Lübbenau<br>Ortsteil Lehde<br><a class="link" href="tel:{SITE["tel_href"]}">{SITE["tel"]}</a><br><a class="link" href="mailto:{SITE["mail"]}">{SITE["mail"]}</a></address>
    {link_arrow('Nachricht schreiben', '/kontakt/')}
  </article>
</div>''')

    ld = {"@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Mutschenhof",
          "description": META['home']['desc'], "url": SITE['url'] + '/', "telephone": "+4915155322032", "email": SITE['mail'],
          "address": {"@type": "PostalAddress", "streetAddress": "Kaupen 9b", "postalCode": "03222",
                      "addressLocality": "Lübbenau/Spreewald (Ortsteil Lehde)", "addressCountry": "DE"},
          "sameAs": [SITE['facebook'], SITE['instagram']]}
    return dict(slug='', title='Mutschenhof im Spreewald – Ferienwohnungen, Kahnfahrten, Hofschlachtung in Lehde',
                desc=META['home']['desc'], hero=True, og='hero-kahn-rinder', jsonld=ld,
                body=hero + welcome + tiles + year + kahn + wohnen + tiere + schlacht + foej_anfahrt)
