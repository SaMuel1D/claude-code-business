import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Tägliche Prüfzeit (24h-Format, Lokalzeit)
CHECK_HOUR = int(os.getenv("CHECK_HOUR", "8"))
CHECK_MINUTE = int(os.getenv("CHECK_MINUTE", "0"))

INSTAGRAM_ACCOUNTS = [
    "der_babyladen_erlangen",
    "mellermaerchenzwerge",
    "maibee_neuenhagen",
    "schuetzling_kindersitzladen",
    "baby_oelrichs",
    "babyone_official",
]

STATE_FILE = "state.json"

# Optional: Instagram-Login für zuverlässigeres Scraping
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
