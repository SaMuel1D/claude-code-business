import json
import os
from datetime import datetime
from config import STATE_FILE


def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, default=str)


def get_last_seen(state: dict, account: str) -> str | None:
    return state.get(account, {}).get("last_post_shortcode")


def update_account(state: dict, account: str, shortcode: str, timestamp: datetime):
    state[account] = {
        "last_post_shortcode": shortcode,
        "last_post_time": timestamp.isoformat(),
        "last_checked": datetime.now().isoformat(),
    }
