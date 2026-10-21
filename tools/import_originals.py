#!/usr/bin/env python3
"""Einmaliger Import: kopiert die Originalbilder aus dem WordPress-Spiegel nach site/assets/img-src
mit sprechenden Namen. Banner mit eingebranntem Text werden so beschnitten, dass nur das Foto bleibt."""
import sys, shutil
from pathlib import Path
from PIL import Image
U = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/src/wp-content/uploads')
D = Path(__file__).resolve().parent.parent / 'site/assets/img-src'
D.mkdir(parents=True, exist_ok=True)
F = '2022/07/Mutschenhof_Kilka_Fewo_'
M = {  # name: (quelle, crop-box oder None)
 'hero-kahn-rinder':('2022/08/FOeJ.jpg',None), 'hof-kuerbisse':('2022/08/Der_Mutschenhof.jpg',None),
 'rinder-herbst':('2022/08/Schlachtung.jpg',None), 'rinder-wiese':('2022/07/Unsere-Rinder.jpg',None),
 'schweine-huehner':('2023/03/Schweine_Huehner.jpg',None),
 'fliess-1':('2023/03/Kahnfahren-Spreewald-scaled-970x520.jpg',None),'fliess-2':('2023/03/Kahnfahren-Spreewald_2-scaled-970x520.jpg',None),
 'fliess-3':('2023/03/Kahnfahren-Spreewald_3-970x520.jpg',None),'kahn-hund':('2023/03/Kahnfahren-Spreewald_4-970x520.jpg',None),
 'fliess-gruen':('2026/04/Spreewaldfliess.jpg',None),'natur-baeume':('2026/04/Spreewaldnatur.jpg',None),'kuhweide':('2026/04/Kuhweide.jpg',None),
 'kahn-staker':('2026/04/Kahnfahrt-Spreewald.jpg',None),'kahn-hof':('2026/04/Kahnfahrt-Spreewald-Mutschenhof.jpg',None),'kahn-paar':('2026/04/Mutschenhof-Kahnfahrt.jpg',None),
 'fuehrung-hof':('2026/04/Fuehrung.jpg',None),'fuehrung-schweine':('2026/04/artgerechte-Tierhaltung.jpg',None),'fuehrung-stall':('2026/04/hautnah-erleben.jpg',None),
 'foej-julius':('2022/10/Julius.png',None),'foej-lea':('2022/10/Lea.png',None),'foej-fiona':('2024/07/foej.png',None),
 'lischka-terrasse':(F+'Landhaus_Terrasse-1-510x360.jpg',None),'lischka-hof':(F+'Landhaus_Hof-510x360.jpg',None),
 'lischka-esszimmer':(F+'Landhaus_Esszimmer-510x360.jpg',None),'lischka-esszimmer-2':(F+'Landhaus_Esszimmer_2-510x360.jpg',None),
 'lischka-kueche':(F+'Landhaus_Kueche-510x360.jpg',None),'lischka-schlafzimmer':(F+'Landhaus_Schlafzimmer-510x360.jpg',None),
 'lischka-schlafzimmer-2':(F+'Landhaus_Schlafzimmer_2-510x360.jpg',None),'lischka-schlafzimmer-3':(F+'Landhaus_Schlafzimmer_3-510x360.jpg',None),
 'spreewa-terrasse':(F+'Rustikal_Terrasse-510x360.jpg',None),'spreewa-esszimmer':(F+'Rustikal_Esszimmer-1-510x360.jpg',None),
 'spreewa-kueche':(F+'Rustikal_Kueche-510x360.jpg',None),'spreewa-schlafzimmer':(F+'Rustikal_Schlafzimmer-510x360.jpg',None),
 'spreewa-schlafzimmer-2':(F+'Rustikal_Schlafzimmer_2-510x360.jpg',None),
 'lehde':('2022/07/Lehde_Spreewald.jpg',None),'kahn-lehde':('2022/07/Kahnfahrt_Spreewald.jpg',None),
 'luebbenau-ortskern':('2022/07/historischer_Ortskern_Luebbenau.jpg',None),'spreewaldhafen':('2022/07/Grosser_Hafen.jpg',None),
 'branitz':('2022/07/Schloss_Branitz.jpg',None),'spreewelten':('2022/07/spreewelten_luebbenau.jpg',None),
 'hof-fachwerk':('2022/10/Homepage_Mutschenhof.png',(0,120,510,360)),
 'steak':('2023/04/Slider_Schlachterei.png',(0,250,970,520)),'salami':('2022/10/Slider_Geschmack.png',(330,230,970,520)),
 'wurst':('2022/10/Wurstwaren.jpg',(0,0,510,295)),'zerlegen':('2022/10/frisch-geschlachtet.jpg',(0,0,510,290)),
 'anfahrt-karte':('2023/04/Anfahrt-Mutschenhof.png',None),
 'flyer-termine':('2025/08/Schlachtetermine-25-26_neu.png',None),'flyer-rindfleisch':('2025/08/Flyer-Schlachtetermine-25-26_neu.png',None),
 'badge-referenzbetrieb':('2025/07/Referenzbetrieb-Spreewald.png',None),
}
for k,(s,box) in M.items():
    im = Image.open(U/s)
    if box: im = im.crop(box)
    ext = 'png' if k in('anfahrt-karte','flyer-termine','flyer-rindfleisch','badge-referenzbetrieb') else 'jpg'
    if ext=='jpg': im.convert('RGB').save(D/f'{k}.jpg',quality=95,subsampling=0)
    else: im.save(D/f'{k}.png')
# Logo: Original (grün/dunkelgrau) + helle Variante für dunkle Flächen
lg = Image.open(U/'2022/08/Logo-Mutschenhof.png').convert('RGBA')
bbox = lg.getbbox(); lg = lg.crop(bbox); lg.thumbnail((900,900)); lg.save(D/'logo.png')
px = lg.load(); l2 = lg.copy(); p2 = l2.load()
for y in range(lg.height):
    for x in range(lg.width):
        r,g,b,a = px[x,y]
        if a and max(r,g,b) < 110 and abs(r-g) < 25:   # dunkelgrau -> creme
            p2[x,y] = (245,239,224,a)
l2.save(D/'logo-hell.png')
print(len(list(D.iterdir())),'Dateien in',D)
