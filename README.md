# Mutschenhof – neue Website

Statische, mehrseitige Website (HTML/CSS/JS) für den Mutschenhof in Lehde/Spreewald.
Inhalte und Fotos stammen vollständig aus der bisherigen WordPress-Seite. Keine Cookies, kein Tracking,
keine externen Schriften; externe Inhalte (YouTube, fungiwo-Kalender) werden erst nach Klick geladen.

## Lokal starten
```
python3 build.py                      # erzeugt den Ordner dist/ (Python 3 + Pillow)
python3 -m http.server 8000 -d dist   # Vorschau unter http://localhost:8000
```

## Veröffentlichen
Den **Inhalt von `dist/`** auf den Webspace laden (FTP/SFTP) – fertig. Es ist kein Server-Programm nötig.
Die Seiten-Adressen entsprechen den bisherigen (`/ferienwohnungen/`, `/kahnfahrten/` …), Weiterleitungen sind daher nicht nötig.
Domain für Canonical-Links/Sitemap: `SITE['url']` in `site/lib.py`.

## Inhalte pflegen
| Was | Wo |
|---|---|
| Texte der Seiten | `site/p_*.py` (Originaltexte stehen in `site/content.json`) |
| Schlachttermine | `site/data/schlachttermine.json` – neue Termine als `JJJJ-MM-TT` eintragen, die Seite zeigt automatisch Countdown |
| Bilder | `site/assets/img-src/` (Dateinamen beibehalten oder in `p_*.py` anpassen); danach `python3 build.py` |
| Farben/Schriften | `site/assets/css/main.css` (`:root`) |
| Kontaktdaten, Links | `SITE` in `site/lib.py` |

## Offene Punkte (bitte klären)
1. **Datenschutzerklärung** ist der Text vom Stand Januar 2023 (teils durcheinander im Original, Aufzählung zur Logfile-Speicherung wurde an ihren Platz gesetzt) und erwähnt Cookies. Bitte rechtlich prüfen/aktualisieren lassen. Ergänzt wurde nur ein sachlicher Abschnitt zu den per Klick geladenen externen Inhalten.
2. **Widersprüchliche Kontaktdaten im Original:** Impressum: 0151 55 322 032 und info@mutschenhof.de – Datenschutz: 03542/45816 und info@mutschenhof-spreewald.de. Auf der Website werden die Impressums-Daten verwendet.
3. **Schlachttermine:** vorhanden sind nur die Termine 2025/26 (alle vorbei). Neue Termine eintragen (siehe oben).
4. **Formulare** (Kahnfahrt, Kontakt) öffnen das E-Mail-Programm mit vorbereiteter Nachricht an info@mutschenhof.de. Für echten Versand ohne Mailprogramm wird ein Server-Skript oder Formulardienst benötigt. Der Zustimmungstext zum Datenschutz ist neu formuliert.
5. **Hofführung online buchen:** Der Link `localtour.checkfront.com/reserve/?item_id=758` wurde aus den Widget-Angaben der alten Seite abgeleitet (`SITE['checkfront']`) – bitte testen.
6. **Fehlende Angaben in der Quelle (bewusst nicht ergänzt):** Preise der Ferienwohnungen, Preis/Termine der Hofführung, Öffnungszeiten, Schlachterei-Preise.
7. **Bildqualität/-rechte:** Ferienwohnungsfotos liegen nur in 510 px, einige Kahn-Fotos in 540 px vor – größere Originale einsetzen. Auf Fotos sind Personen (Hofführung, FÖJ, Kahnfahrten): Nutzungsrechte/Einwilligungen bitte prüfen.
8. **Zahlen, die sich ändern können:** „zurzeit 24 Rinder“ (Tierhaltung/Startseite).
9. **Originaltexte unverändert übernommen, inkl. Tippfehlern**, z. B. „denkmalgeschützen“, „aufgewegte Bande“, „Mit unser ökologisch und nachhaltigen Landwirtschaft“, „unteranderem“, „d ‚Aquitaine“, „Kahnfahrschule … Mit unser …“.
10. Der Zwischenstand „Ein Jahr auf der Insel“ (Startseite) fasst Aussagen der Seiten Landwirtschaft/Tierhaltung zusammen; die Überschrift „Zur Erntezeit“ ist bewusst ohne Monat.
