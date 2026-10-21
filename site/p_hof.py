from lib import *

def pf(key, alt, ratio='ar-43', sizes='(max-width:860px) 92vw, 46vw', **kw):
    return f'<div class="frame"><div class="pic {ratio} pic--shadow">{img(key, alt, sizes, widths=[480, 800, 1200], **kw)}</div></div>'

def build():
    pages = []

    # ---------------------------------------------------------------- Der Mutschenhof
    s = 'der-mutschenhof'
    body = phero('Die Familie', blk(s, 1), 'Der Mutschenhof', img('hof-kuerbisse', 'Kürbisse am Ufer, daneben ein Kahn am Steg', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 800, 1200], pos='25% 50%'),
                 crumbs=[('Der Hof', '/der-mutschenhof/')], ratio='ar-45')
    body += section(f'''
<div class="split split--wide-text split--top">
  <div class="prose">
    {reveal(paras(s, 2, 3))}
    {reveal(f'<figure class="quote" style="margin:2.5rem 0"><blockquote>{blk(s, 3)}</blockquote></figure>')}
    {reveal(paras(s, 4, 5))}
  </div>
  <div class="stack">
    {reveal(pf('hof-fachwerk', 'Fachwerkhaus mit grünen Fensterläden am Wasser', 'ar-169', pos='50% 40%'))}
    {reveal('<div class="card"><h3>Zum Hof gehören</h3><ul class="chips"><li>Rinder</li><li>Schweine</li><li>Hühner</li><li>Katzen</li><li>Hündin Wanda</li><li>Pfau Rex</li></ul></div>')}
  </div>
</div>
<div class="facts reveal" style="margin-top:clamp(3rem,6vw,5rem)">
  <div class="fact"><b>5.</b><span>Generation der Familie Kilka</span></div>
  <div class="fact"><b>2009</b><span>übernahmen Sebastian und Anja Kilka die Führung des Hofs</span></div>
  <div class="fact"><b>4</b><span>Kinder, die den Hof freudig unterstützen</span></div>
  <div class="fact"><b>2018</b><span>ließen wir uns einen „Prahm“ anfertigen – unseren Lastenkahn</span></div>
</div>''')
    body += more([('/oekologische-landwirtschaft/', 'Der Hof', 'Ökologische Landwirtschaft', 'Mit dem Kahn zu Äckern und Wiesen – wie vor hundert Jahren.'),
                  ('/artgerechte-tierhaltung/', 'Der Hof', 'Artgerechte Tierhaltung', 'Rinder, Schweine und Hühner auf dem Mutschenhof.'),
                  ('/hoffuehrung/', 'Erleben', 'Hofführungen', 'Hofgeflüster – lauschen Sie den Stimmen des Hofes.')])
    pages.append(dict(slug=s, title='Der Mutschenhof', desc=META[s]['desc'], body=body, og='hof-kuerbisse'))

    # ---------------------------------------------------------------- Ökologische Landwirtschaft
    s = 'oekologische-landwirtschaft'
    body = phero('Ökologische Landwirtschaft', blk(s, 1), 'Der Hof', img('fliess-1', 'Ein grünes Spreewaldfließ zwischen hohen Bäumen', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 800, 970], pos='45% 50%'),
                 crumbs=[('Der Hof', '/der-mutschenhof/')], ratio='ar-45')
    body += section(rows([
        ('Mit der Natur arbeiten', paras(s, 2, 6), pf('rinder-herbst', 'Rinder auf einer herbstlichen Weide', 'ar-43')),
        ('Äcker auf Inseln', paras(s, 6, 10), pf('hero-kahn-rinder', 'Mit dem Kahn über ein Fließ, am Ufer grasen Rinder', 'ar-43', pos='40% 50%')),
        ('Inselhüpfen, Heu und Ernte', paras(s, 10, 13), pf('hof-kuerbisse', 'Kürbisse am Ufer neben einem Kahn', 'ar-43', pos='30% 50%')),
        ('Der Winterstau', paras(s, 13, 15), pf('rinder-wiese', 'Rinder grasen an einem Fließ', 'ar-43')),
    ]))
    body += more([('/artgerechte-tierhaltung/', 'Der Hof', 'Artgerechte Tierhaltung', 'Die Mutschen, Schweine und Hühner.'),
                  ('/hofeigene-schlachtung/', 'Schlachterei', 'Vom eigenen Hof', 'Spreewälder Rindfleisch aus hofeigener Schlachtung.'),
                  ('/hoffuehrung/', 'Erleben', 'Hofführungen', 'Sämtliche Arbeiten erledigen wir mit dem Kahn – erleben Sie es.')])
    pages.append(dict(slug=s, title='Ökologische Landwirtschaft', desc=META[s]['desc'], body=body, og='fliess-1'))

    # ---------------------------------------------------------------- Artgerechte Tierhaltung
    s = 'artgerechte-tierhaltung'
    body = phero('Artgerechte Tierhaltung', '', 'Der Hof', img('rinder-wiese', 'Rinder grasen an einem Fließ', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 800, 1080], pos='55% 50%'),
                 crumbs=[('Der Hof', '/der-mutschenhof/')], ratio='ar-45')
    body = body.replace('<p class="lede"></p>', '')
    body += section(f'''
<div class="facts reveal">
  <div class="fact"><b>24</b><span>Rinder in der Herde – zurzeit</span></div>
  <div class="fact"><b>Blonde d’Aquitaine</b><span>die Rasse unserer „Mutschen“</span></div>
  <div class="fact"><b>Hörner</b><span>dürfen die Rinder bei uns behalten</span></div>
  <div class="fact"><b>Mutterkuh</b><span>Die Rinder wachsen in Mutterkuhhaltung auf</span></div>
</div>''', cls='section--tight')
    body += section(rows([
        ('Rinder', '<p>' + strip_head(blk(s, 1)) + '</p>' + paras(s, 2, 4), pf('rinder-herbst', 'Rinder auf einer herbstlichen Weide', 'ar-43')),
        ('Schweine', '<p>' + strip_head(blk(s, 5)) + '</p>', f'<div class="frame arch"><div class="pic ar-45">{img("fuehrung-schweine", "Zwei Kinder füttern Schweine im Stall", "(max-width:860px) 80vw, 36vw", widths=[360, 426])}</div></div>'),
        ('Hühner', '<p>' + blk(s, 7) + '</p>', pf('schweine-huehner', 'Schweine und Hühner fressen gemeinsam auf der Wiese', 'ar-169')),
    ]))
    body += more([('/hoffuehrung/', 'Erleben', 'Hofführungen', 'Erleben Sie artgerechte Tierhaltung hautnah.'),
                  ('/oekologische-landwirtschaft/', 'Der Hof', 'Ökologische Landwirtschaft', 'Mit dem Kahn zu Äckern und Wiesen.'),
                  ('/hofeigene-schlachtung/', 'Schlachterei', 'Das Schlachthaus', 'Keine langen und stressigen Tiertransporte.')])
    pages.append(dict(slug=s, title='Artgerechte Tierhaltung', desc=META[s]['desc'], body=body, og='rinder-herbst'))

    # ---------------------------------------------------------------- FÖJ
    s = 'freiwilliges-oekologisches-jahr-foej'
    body = phero('Freiwilliges ökologisches Jahr', blk(s, 1), 'Mitarbeiten auf dem Hof', img('foej-lea', 'Eine Freiwillige schmiegt sich an ein Kalb im Stroh', '(max-width:860px) 90vw, 40vw', eager=True, widths=[480, 510], pos='50% 40%'),
                 crumbs=[('Der Hof', '/der-mutschenhof/')], ratio='ar-43', actions=btn('Jetzt bewerben', '/kontakt/'))
    voices = ''
    for i, (name, key, q, y) in enumerate([('Julius', 'foej-julius', 5, 6), ('Lea', 'foej-lea', 7, 8), ('Fiona', 'foej-fiona', 9, 10)]):
        voices += (f'<figure class="voice reveal" style="--d:{i*.1}s"><div class="pic">{img(key, "Porträt von " + name, "(max-width:900px) 92vw, 30vw", widths=[360, 510], pos="50% 30%")}</div>'
                   f'<div class="voice-body"><blockquote>{blk(s, q)}</blockquote><cite>{name}<span>{blk(s, y)}</span></cite></div></figure>')
    body += section(f'''
<div class="split split--wide-text split--top"><div class="prose">{reveal(paras(s, 2, 5))}{reveal(btn("Jetzt bewerben", "/kontakt/"))}</div>
<div class="reveal" style="--d:.1s">{pf('foej-fiona', 'Eine Freiwillige mit Hund im Boot', 'ar-43', pos='50% 40%')}</div></div>''')
    body += section(f'<div class="head center">{eyebrow("Stimmen")}<h2>Das sagen unsere Freiwilligen</h2></div><div class="voices">{voices}</div>', cls='section--alt', wave_top='--cream-2')
    pages.append(dict(slug=s, title='Freiwilliges ökologisches Jahr (FÖJ)', desc=META[s]['desc'], body=body, og='foej-lea'))
    return pages
