# /shutdown — Session beenden & alles sichern

Fasse die Session zusammen, sichere alle Änderungen und bereite den Workspace für die nächste Session vor.

## Schritte

1. **Session-Rückblick erstellen**
   Schaue auf den Verlauf dieser Session und beantworte:
   - Was wurde besprochen / bearbeitet?
   - Welche Entscheidungen wurden getroffen?
   - Was wurde konkret erledigt (Dateien erstellt, geändert, gelöscht)?
   - Was ist offen geblieben?

2. **Inbox prüfen**
   - Zeige alle Dateien in `inbox/` an
   - Frag: "Soll ich etwas davon in context/ oder plans/ übertragen, oder bleibt es für die nächste Session?"
   - Verarbeite entsprechend der Antwort

3. **Context-Dateien aktualisieren**
   Prüfe ob neue Informationen aus der Session in diese Dateien gehören:
   - `context/current-data.md` — neue Metriken, Status-Updates
   - `context/strategy.md` — geänderte Prioritäten, neue Entscheidungen
   - `context/personal-info.md` / `context/business-info.md` — strukturelle Änderungen
   Nimm Updates nur vor, wenn es wirklich neue, relevante Information gibt.

4. **CLAUDE.md prüfen**
   Falls neue Commands, Ordner oder Workspace-Strukturen entstanden sind: CLAUDE.md entsprechend aktualisieren.

5. **Session-Log speichern**
   Erstelle `outputs/session-log-YYYY-MM-DD.md` mit:

```markdown
# Session-Log [Datum]

## Bearbeitet
- 

## Entscheidungen
- 

## Offen / nächste Session
- 

## Geänderte Dateien
- 
```

6. **Abschluss-Nachricht**
   Gib aus:
   - Zusammenfassung in 2-3 Sätzen
   - Liste der aktualisierten/erstellten Dateien
   - Den einen wichtigsten offenen Punkt für die nächste Session

---

Halte alles präzise. Kein Fließtext-Padding. Die nächste Session startet mit `/start` — diese Logs und Updates sind der Kontext.
