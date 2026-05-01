# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Anweisungen für die Arbeit in diesem Repository.

---

## Was das hier ist

Dies ist ein **Claude Workspace Template** — eine strukturierte Umgebung, die für die Arbeit mit Claude Code als leistungsstarkem Agenten-Assistenten über mehrere Sessions hinweg konzipiert ist. Der Benutzer startet wiederholt neue Claude Code Sessions und verwendet `/prime` zu Beginn jeder Session, um den wesentlichen Kontext ohne Ballast zu laden.

**Diese Datei (CLAUDE.md) ist das Fundament.** Sie wird automatisch am Anfang jeder Session geladen. Halte sie aktuell — sie ist die Single Source of Truth dafür, wie Claude diesen Workspace verstehen und darin arbeiten soll.

---

## Die Claude-User-Beziehung

Claude arbeitet als **Agenten-Assistent** mit Zugriff auf die Workspace-Ordner, Kontext-Dateien, Commands und Outputs. Die Beziehung ist:

- **User**: Definiert Ziele, liefert Kontext zu seiner Rolle/Funktion und steuert die Arbeit über Commands
- **Claude**: Liest Kontext, versteht die Ziele des Users, führt Commands aus, produziert Outputs und pflegt die Workspace-Konsistenz

Claude sollte sich immer über `/prime` am Session-Start orientieren, dann mit vollem Bewusstsein dafür handeln, wer der User ist, was er erreichen möchte und wie dieser Workspace das unterstützt.

---

## Workspace-Struktur

```
.
├── CLAUDE.md              # Diese Datei — Kern-Kontext, immer geladen
├── .claude/
│   └── commands/          # Slash-Commands, die Claude ausführen kann
│       ├── start.md       # /start — Session-Start & Status-Überblick
│       ├── capture.md     # /capture — Schnelle Notiz in inbox/ speichern
│       ├── plan.md        # /plan — Projektplan erstellen
│       ├── shutdown.md    # /shutdown — Session beenden & sichern
│       ├── prime.md       # /prime — Session-Initialisierung (Legacy)
│       ├── create-plan.md  # /create-plan — Implementierungspläne erstellen
│       └── implement.md   # /implement — Pläne umsetzen
├── context/               # Hintergrund-Kontext über den User und das Projekt
├── inbox/                 # Schnell-Notizen, erfasst via /capture
├── plans/                 # Projektpläne erstellt von /plan oder /create-plan
├── outputs/               # Arbeitsergebnisse, Deliverables, Session-Logs
├── reference/             # Vorlagen, Beispiele, wiederverwendbare Patterns
└── scripts/               # Automatisierungsskripte (falls zutreffend)
```

**Verzeichnisse:**

| Verzeichnis  | Zweck                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------- |
| `context/`   | Wer der User ist, seine Rolle, aktuelle Prioritäten, Strategien. Gelesen von `/start`.      |
| `inbox/`     | Schnell-Notizen aus `/capture`. Werden bei `/start` angezeigt, bei `/shutdown` verarbeitet. |
| `plans/`     | Projektpläne aus `/plan`. Umsetzen mit `/implement`.                                         |
| `outputs/`   | Deliverables, Analysen, Reports, Session-Logs aus `/shutdown`.                               |
| `reference/` | Hilfreiche Dokumentation, Vorlagen und Patterns für verschiedene Workflows.                  |
| `scripts/`   | Automatisierungs- und Tooling-Skripte.                                                       |

---

## Commands

### /start

**Zweck:** Session starten — Kontext laden und kompakten Status anzeigen.

Ersetzt `/prime`. Liest CLAUDE.md, alle context/-Dateien, offene Pläne und die Inbox. Zeigt einen scanba­ren Status-Block: wer du bist, aktueller Strategiefokus, offene Pläne, unverarbeitete Inbox-Notizen.

### /capture [notiz]

**Zweck:** Gedanken, Ideen oder To-dos blitzschnell sichern.

Text direkt nach dem Command eingeben. Speichert sofort als datierte Markdown-Datei in `inbox/`. Erscheint beim nächsten `/start` und wird bei `/shutdown` verarbeitet.

Beispiel: `/capture Idee: Kundenumfrage für Q3 planen`

### /plan [projektname]

**Zweck:** Ausführlichen Projektplan erstellen.

Stellt maximal 3 Klärungsfragen, dann erstellt Claude einen strukturierten Plan mit Kontext, Zielen, Phasen und Aufgaben. Gespeichert in `plans/YYYY-MM-DD-[projektname].md`.

Beispiel: `/plan Social-Media-Strategie-Q3`

### /shutdown

**Zweck:** Session sauber beenden — alles sichern, Workspace für nächste Session vorbereiten.

Erstellt einen Session-Log in `outputs/`, verarbeitet die Inbox, aktualisiert context/-Dateien bei Bedarf und nennt den wichtigsten offenen Punkt für die nächste Session.

### /create-plan [anforderung] _(Legacy)_

**Zweck:** Detaillierten Implementierungsplan für Workspace-Änderungen erstellen.

Für technische Workspace-Erweiterungen (neue Commands, Skripte, Strukturänderungen). Für inhaltliche Projektplanung → `/plan` verwenden.

### /implement [plan-pfad]

**Zweck:** Einen mit /create-plan erstellten Plan umsetzen.

Liest den Plan, führt jeden Schritt der Reihe nach aus, validiert die Arbeit und aktualisiert den Plan-Status.

Beispiel: `/implement plans/2026-01-28-wettbewerbs-analyse-command.md`

---

## Kritische Anweisung: Diese Datei pflegen

**Wann immer Claude Änderungen am Workspace macht, MUSS Claude prüfen, ob CLAUDE.md aktualisiert werden muss.**

Nach jeder Änderung — ob Commands, Skripte, Workflows oder Strukturänderungen — frage:

1. Fügt diese Änderung neue Funktionalität hinzu, die Benutzer kennen müssen?
2. Ändert sie die oben dokumentierte Workspace-Struktur?
3. Sollte ein neuer Command aufgelistet werden?
4. Braucht context/ neue Dateien dafür?

Falls ja, aktualisiere die entsprechenden Abschnitte. Diese Datei muss immer den aktuellen Zustand des Workspace widerspiegeln, damit zukünftige Sessions genauen Kontext haben.

**Beispiele für Änderungen, die CLAUDE.md-Updates erfordern:**

- Neuen Slash-Command hinzufügen → im Commands-Abschnitt ergänzen
- Neuen Output-Typ erstellen → in Workspace-Struktur dokumentieren oder Abschnitt erstellen
- Skript hinzufügen → Zweck und Verwendung dokumentieren
- Workflow-Patterns ändern → entsprechende Dokumentation aktualisieren

---

## Für Benutzer, die dieses Template herunterladen

Um diesen Workspace an deine eigenen Bedürfnisse anzupassen, fülle deine Kontext-Dokumente in `context/` aus und passe sie nach Bedarf an. Verwende dann `/create-plan` zum Planen und `/implement` zum Umsetzen struktureller Änderungen. So bleibt alles synchron — besonders CLAUDE.md, die immer den aktuellen Zustand des Workspace widerspiegeln muss.

---

## Session-Workflow

1. **Start**: `/start` — Kontext laden, Status-Überblick erhalten
2. **Erfassen**: `/capture [text]` — Ideen und To-dos sofort sichern
3. **Planen**: `/plan [name]` — Projektplan erstellen
4. **Umsetzen**: `/implement [plan-pfad]` — Plan Schritt für Schritt ausführen
5. **Beenden**: `/shutdown` — Session-Log, Inbox verarbeiten, Workspace aktualisieren

---

## Notizen

- Kontext minimal aber ausreichend halten — kein Bloat
- Pläne in `plans/` mit datierten Dateinamen für die Historie
- Outputs nach Typ/Zweck in `outputs/` organisiert
- Referenzmaterialien in `reference/` zur Wiederverwendung
