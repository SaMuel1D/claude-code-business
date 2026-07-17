# Claude Project „Kindersitz-Beratung" — Einrichtung für Mitarbeiterin

Erstellt: 2026-05-18  
Zweck: Mitarbeiterin hat auf Android/iPad schnellen Zugriff auf alle Beratungsunterlagen

---

## Was ein Claude Project ist

Ein Claude Project ist wie ein eigener Assistent mit eingebautem Gedächtnis:
- Du lädst einmal alle wichtigen Dokumente hoch
- Claude liest sie und kennt den Inhalt
- Die Mitarbeiterin tippt einfach eine Frage — z.B. „Passt der BeSafe iZi Twist in einen Renault Scenic 2018?" — und bekommt sofort die Antwort

---

## Schritt 1 — Claude Pro aktivieren (falls noch nicht)

- claude.ai aufrufen → Plan upgraden auf **Pro** (20 €/Monat)
- Projects sind ein Pro-Feature

---

## Schritt 2 — Neues Project anlegen

1. claude.ai öffnen
2. Links in der Sidebar: **„Projects"** → **„New Project"**
3. Name: `Kindersitz-Beratung Familie Bär`
4. Auf **„Project instructions"** klicken (das ist der System-Prompt)

---

## Schritt 3 — Diesen System-Prompt einfügen

Kopiere diesen Text in das Feld „Project instructions":

---

```
Du bist die Beratungsassistentin von Familie Bär, einem spezialisierten Kindersitz-Fachhandel. 
Du hilfst der Mitarbeiterin schnell und präzise bei Kundenfragen.

Deine Aufgaben:
- Produktinfos zu Kindersitzen aus den hochgeladenen Datenblättern nachschlagen
- Kompatibilitäten zwischen Sitzen und Autos prüfen
- ISOFIX-Infos, Gewichts- und Größengrenzen nennen
- Beratungshinweise aus dem Beratungsleitfaden geben

Antworte immer:
- Kurz und präzise — die Mitarbeiterin ist mitten in der Beratung
- Auf Deutsch
- Mit klarer Quellenangabe (z.B. „laut Datenblatt BeSafe iZi Twist")
- Falls eine Info nicht in den Dokumenten steht: Klar sagen „das steht nicht in meinen Unterlagen"

Du gibst keine Preise bekannt und keine Kaufempfehlungen ohne Rückfrage an Sandra.
```

---

## Schritt 4 — Diese Dateien hochladen (Priorität 1 — unbedingt)

Pfad: `reference/Pinker Ordner Familie Bär/`

| Ordner | Datei | Warum |
|--------|-------|-------|
| `2. Beratung/` | `Beratungsleitfaden.pdf` | Kern-Leitfaden für die Beratung |
| `2. Beratung/` | `Beratungsprotokoll.pdf` | Struktur der Beratung |
| `3. Kindersitz Datenblätter/` | `3. Isofix Größenklassen.pdf` | Häufig gefragt |
| `3. Kindersitz Datenblätter/3. Babyschalen/` | Alle `.docx` Dateien | Produktinfos Babyschalen |
| `3. Kindersitz Datenblätter/3. Reboarder/` | Alle `.docx` Dateien | Produktinfos Reboarder |
| `3. Kindersitz Datenblätter/3. Folgesitze/` | Alle `.docx` Dateien | Produktinfos Folgesitze |

**Hinweis:** Claude Projects unterstützt PDF und DOCX. Je mehr Datenblätter, desto besser die Antworten.

---

## Schritt 5 — Diese Dateien hochladen (Priorität 2 — sehr hilfreich)

| Ordner | Inhalt |
|--------|--------|
| `4. Autofragen/` | Auto-Kompatibilitäts-Infos |
| `6. Testergebnisse/` | Crashtest-Ergebnisse |
| `9. Fliegen mit Kind/` | Airline-Bedingungen |
| `reference/Autohandbücher verstehen/` | ISOFIX, Autohandbücher finden |

---

## Schritt 6 — Mitarbeiterin Zugriff geben

**Option A — Geteilter Login (einfachste Lösung):**
- Du gibst ihr die Login-Daten für dein Claude-Konto
- Sie öffnet claude.ai auf ihrem Handy/iPad im Browser
- Sie wählt das Project „Kindersitz-Beratung Familie Bär"
- Fertig

**Option B — Eigener Account (sauberer):**
- Mitarbeiterin erstellt kostenlosen Claude-Account
- Du teilst das Project mit ihr (in Project-Settings → „Invite")
- ⚠️ Dafür braucht sie keinen eigenen Pro-Account, wenn du das Project geteilt hast

---

## So benutzt die Mitarbeiterin das Project

Sie tippt einfach natürliche Fragen, z.B.:

> „Welche Babyschalen haben wir von Maxi-Cosi?"

> „Bis wie viel kg geht der BeSafe iZi Twist?"

> „Passt der Axkid Minikid in einen Smart 2014?"

> „Was sind die Airline-Bedingungen für Flugreisen mit Kindersitz?"

> „Zeig mir den Beratungsablauf"

---

## Wichtige Hinweise

- **Dateien aktuell halten:** Wenn du neue Datenblätter bekommst, einfach in das Project hochladen
- **Kein PC nötig:** Die Mitarbeiterin braucht nur ihr Handy/iPad und eine Internetverbindung
- **Datenschutz:** Kundendaten (Namen, Adressen) NICHT in das Project hochladen — nur Produkt- und Beratungsunterlagen

---

## Nächste Schritte

1. [ ] Claude Pro aktivieren oder bestätigen dass aktiv
2. [ ] Project anlegen + System-Prompt einfügen
3. [ ] Datenblätter aus Ordner `3. Kindersitz Datenblätter/` hochladen
4. [ ] Beratungsleitfaden + Protokoll hochladen
5. [ ] Mitarbeiterin zeigen wie sie das Project öffnet
6. [ ] Testfragen stellen um sicherzustellen dass alles funktioniert
