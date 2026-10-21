# Vorschau über GitHub ansehen (Schritt für Schritt)

Ziel: Die Website liegt in einem **privaten** GitHub-Repository, und GitHub Pages zeigt die Vorschau unter einer Internetadresse an, die Sie am Handy öffnen.

**Wichtig vorab:** GitHub Pages aus einem *privaten* Repository gibt es nur mit bezahltem Konto (GitHub Pro, ca. 4 US-$/Monat; Preis bitte auf github.com/pricing prüfen). Mit dem kostenlosen Konto muss das Repository öffentlich sein. Die Pages-Adresse selbst ist auch bei privatem Repository für jeden aufrufbar, der sie kennt (die Vorschau enthält `noindex`, Google nimmt sie also nicht auf). Wer die Vorschau wirklich geheim halten will, nutzt Weg B oder C unten.

## Weg A: GitHub Desktop + GitHub Pages

1. **Konto:** Auf github.com anmelden oder kostenlos registrieren.
2. **GitHub Desktop** installieren (desktop.github.com), starten und mit dem Konto anmelden (File → Options → Accounts).
3. **ZIP entpacken:** `mutschenhof-projekt.zip` auf dem Computer entpacken, z. B. nach `Dokumente/mutschenhof-website`.
4. **Repository anlegen:** In GitHub Desktop *File → Add local repository…* → den entpackten Ordner wählen. Kommt die Meldung „not a Git repository“, auf *create a repository* klicken.
   - Name: `mutschenhof-website`
   - **Haken bei „Keep this code private“ setzen** (kommt im nächsten Schritt).
5. **Erster Commit:** Links stehen alle Dateien. Unten Zusammenfassung „Erste Version der neuen Website“ eintragen → *Commit to main*.
6. **Hochladen:** Oben *Publish repository* → Haken bei **Keep this code private** lassen → *Publish*.
7. **Pages einschalten:** Auf github.com das Repository öffnen → *Settings* → links *Pages* → bei *Build and deployment* → *Source: Deploy from a branch* → *Branch: main*, Ordner **/docs** → *Save*.
   - Erscheint die Auswahl nicht oder meldet GitHub, dass Pages für private Repositories nicht verfügbar ist: Konto auf Pro umstellen oder Weg B/C nehmen.
8. **Warten:** Nach 1–2 Minuten steht oben auf der Pages-Seite „Your site is live at https://IHR-NAME.github.io/mutschenhof-website/“. Diese Adresse am Handy öffnen.

## Wenn Sie etwas ändern (z. B. neue Schlachttermine)

1. Datei ändern (z. B. `site/data/schlachttermine.json`).
2. Im Ordner ausführen: `python3 build.py` und danach `python3 tools/make_preview.py`.
3. GitHub Desktop → Commit → *Push origin*. Nach 1–2 Minuten ist die Vorschau aktualisiert.

## Weg B: Privat bleiben, kostenlos (Netlify oder Cloudflare Pages)

Beide Dienste verbinden sich mit dem privaten Repository und bauen die Seite selbst. Einstellungen: Build-Befehl `python3 build.py`, Ausgabeordner `dist`. Die Adresse ist ebenfalls öffentlich abrufbar, aber das Repository bleibt privat und kostenlos.

## Weg C: Nur auf dem eigenen Rechner

Im Projektordner: `python3 build.py`, dann `python3 -m http.server 8000 -d dist` und `http://localhost:8000` öffnen. Am Handy geht das im selben WLAN über `http://IP-DES-RECHNERS:8000`.

## Später: echte Veröffentlichung

Für mutschenhof-spreewald.de wird **nicht** `docs/` verwendet, sondern der Inhalt von `dist/` beim Hoster hochgeladen (siehe README).
