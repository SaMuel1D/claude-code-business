# Instagram Monitor Bot — Setup

## Was der Bot macht
- Prüft täglich (Standard: 8:00 Uhr) alle 6 Instagram-Accounts auf neue Posts & Videos
- Prüft die **Meta Ad Library** auf aktive Anzeigen dieser Accounts — auch solche, die nicht für dich als Zielgruppe geschaltet sind
- Sendet alle Ergebnisse direkt in deinen Telegram-Chat

## Einrichtung (5 Minuten)

### Schritt 1: Telegram Bot erstellen
1. Öffne Telegram, suche **@BotFather**
2. Schreibe `/newbot` und folge den Anweisungen
3. Kopiere deinen **Bot Token** (sieht aus wie `1234567890:ABCdef...`)

### Schritt 2: Deine Chat-ID herausfinden
1. Suche in Telegram nach **@userinfobot**
2. Schreibe `/start` — er antwortet mit deiner ID (z.B. `123456789`)

### Schritt 3: .env-Datei anlegen
```bash
cp .env.example .env
```
Dann `.env` öffnen und ausfüllen:
```
TELEGRAM_BOT_TOKEN=dein_token
TELEGRAM_CHAT_ID=deine_id
CHECK_HOUR=8
CHECK_MINUTE=0
```

### Schritt 4: Abhängigkeiten installieren
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Schritt 5: Bot starten
```bash
python bot.py
```

Den Bot in Telegram mit `/start` begrüßen, dann läuft er täglich automatisch.

---

## Optionen

### Instagram-Login (empfohlen)
Ohne Login kann Instagram das Scraping nach einer Weile blockieren. Mit einem Zweit-Account (nicht deinem Haupt-Account!) in `.env` eintragen:
```
INSTAGRAM_USERNAME=mein_zweit_account
INSTAGRAM_PASSWORD=passwort
```

### Check-Uhrzeit ändern
In `.env`:
```
CHECK_HOUR=9
CHECK_MINUTE=30
```

### Manueller Check
Im Telegram-Chat einfach `/check` schreiben — sofortiger Check ohne Warten.

---

## Befehle im Chat
| Befehl | Funktion |
|--------|----------|
| `/start` | Bot-Info & überwachte Accounts anzeigen |
| `/check` | Sofortigen Check starten |
| `/status` | Letzter gesehener Post je Account |

---

## Dauerhaft laufen lassen (Mac)

Mit einem Launch Agent dauerhaft im Hintergrund starten:
```bash
# Pfad zur venv anpassen!
cat > ~/Library/LaunchAgents/com.instagram-monitor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.instagram-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Pfad/zum/venv/bin/python</string>
        <string>/Users/sandramuller-leschner/Desktop/Claude Code Business/instagram-monitor-bot/bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/sandramuller-leschner/Desktop/Claude Code Business/instagram-monitor-bot</string>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>/tmp/instagram-monitor.log</string>
    <key>StandardErrorPath</key><string>/tmp/instagram-monitor.err</string>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.instagram-monitor.plist
```
