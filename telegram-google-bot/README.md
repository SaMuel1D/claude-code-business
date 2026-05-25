# Telegram Google Bot

Persönlicher Telegram-Bot für Google Kalender & Gmail.

## Funktionen

| Command | Beschreibung |
|---------|-------------|
| `/heute` | Termine für heute |
| `/woche` | Termine für diese Woche |
| `/mails` | Ungelesene Mails (max. 5) |
| `/dringend` | Dringende Mails (URGENT, WICHTIG, markiert) |

---

## Setup (einmalig lokal)

### 1. Google Credentials vorbereiten

In der Google Cloud Console:
- Projekt öffnen → APIs & Dienste → Anmeldedaten
- OAuth-Client-ID erstellen (Typ: **Desktop-App**)
- JSON herunterladen → als `credentials.json` speichern

### 2. Lokal einrichten

```bash
pip install -r requirements.txt

# Credentials bereitstellen
export GOOGLE_CREDENTIALS_PATH=/pfad/zu/credentials.json

# Einmalig OAuth-Flow durchführen (öffnet Browser)
python -c "from google_services import get_credentials; get_credentials()"
# → Meldet dich mit deiner Gmail an, bestätigt den Zugriff
# → Erstellt /tmp/token.json
```

### 3. token.json für Railway sichern

```bash
cat /tmp/token.json
# Inhalt kopieren → wird als Env-Variable in Railway eingefügt
```

---

## Deploy auf Railway

### Environment Variables setzen

| Variable | Wert |
|----------|------|
| `BOT_TOKEN` | Dein Telegram Bot Token (von @BotFather) |
| `TELEGRAM_CHAT_ID` | Deine Telegram Chat-ID (von @userinfobot) |
| `GOOGLE_CREDENTIALS_JSON` | Inhalt deiner `credentials.json` (komplett als Text) |
| `GOOGLE_TOKEN_JSON` | Inhalt deiner `token.json` (komplett als Text) |

### Schritt für Schritt

1. Repository auf GitHub pushen
2. Railway → **New Project** → **Deploy from GitHub repo**
3. Unter **Variables** alle vier Env-Variablen eintragen
4. Deploy starten
5. Unter **Settings** → **Service** sicherstellen dass der Worker läuft (nicht Web)

---

## Lokaler Test

```bash
export BOT_TOKEN=dein_token
export TELEGRAM_CHAT_ID=deine_chat_id
export GOOGLE_CREDENTIALS_PATH=/pfad/zu/credentials.json

python bot.py
```

---

## Deine Chat-ID herausfinden

Schreib in Telegram dem Bot `@userinfobot` — er antwortet mit deiner User-ID.
