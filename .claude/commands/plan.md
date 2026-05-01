# /plan [projektname] — Ausführlichen Projektplan erstellen

Erstelle einen strukturierten Implementierungsplan und lege ihn in `plans/` ab.

## Schritte

1. Lies `context/personal-info.md`, `context/business-info.md` und `context/strategy.md` für Hintergrundkontext
2. Falls der Benutzer noch kein vollständiges Briefing gegeben hat, stelle genau **3 gezielte Klärungsfragen** — nicht mehr — um Lücken zu schließen:
   - Was ist das konkrete Ziel / gewünschte Ergebnis?
   - Was sind die wichtigsten Rahmenbedingungen (Zeit, Budget, Abhängigkeiten)?
   - Was darf auf keinen Fall passieren / was sind No-Gos?
3. Erstelle dann die Plan-Datei unter: `plans/YYYY-MM-DD-[projektname].md`

## Plan-Dateistruktur

```markdown
# Plan: [Projektname]

**Erstellt:** [Datum]
**Status:** Entwurf
**Ziel:** [Ein präziser Satz]

---

## Kontext & Motivation
[Warum dieses Projekt? Was löst es? Einbettung in die Strategie.]

## Ziel & Erfolgskriterien
[Was ist das konkrete Ergebnis? Woran messen wir Erfolg?]

## Rahmenbedingungen
- Zeitrahmen: 
- Budget/Ressourcen: 
- Abhängigkeiten: 
- No-Gos: 

## Aufgaben

### Phase 1: [Name]
- [ ] Aufgabe 1
- [ ] Aufgabe 2

### Phase 2: [Name]
- [ ] Aufgabe 1
- [ ] Aufgabe 2

## Risiken & offene Fragen
- 
- 

## Nächster Schritt
[Die eine konkrete Aktion, die als erstes passieren muss]
```

4. Zeige den Plan direkt in der Antwort an
5. Bestätige: "Plan gespeichert unter `plans/[dateiname]`"
6. Frag, ob wir direkt mit dem nächsten Schritt starten sollen

## Hinweis

Pläne werden mit `/start` aufgelistet. Um einen Plan umzusetzen, verwende `/implement plans/[dateiname]`.
