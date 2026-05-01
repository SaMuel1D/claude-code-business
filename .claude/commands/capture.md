# /capture [notiz] — Schnelle Notiz in Inbox speichern

Speichere eine kurze Notiz sofort in `inbox/` ab, ohne Kontext-Overhead.

## Verhalten

Der Benutzer übergibt den Notiz-Text direkt nach dem Command: `/capture [text]`

1. Nimm den übergebenen Text als Inhalt der Notiz
2. Erstelle eine Datei in `inbox/` mit dem Namensschema: `YYYY-MM-DD-HH-MM-[stichwort].md`
   - Das Stichwort: die ersten 3-4 signifikanten Wörter des Textes, mit Bindestrichen verbunden, lowercase
3. Datei-Inhalt:

```
# [Erster Satz der Notiz als Titel]

**Erfasst:** [Datum und Uhrzeit]

[Vollständiger Notiz-Text]
```

4. Bestätige kurz: Dateiname + "Gespeichert." — kein weiterer Kommentar.

## Wenn kein Text übergeben wurde

Frag einmalig: "Was soll ich erfassen?" — speichere die Antwort dann direkt.

## Hinweis

`/start` zeigt alle inbox/-Dateien beim Session-Start. `/shutdown` fragt, ob Inbox-Einträge verarbeitet oder archiviert werden sollen.
