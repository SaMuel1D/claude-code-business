"""
Instagram Monitor Telegram Bot
Täglich neue Posts + aktive Anzeigen der konfigurierten Accounts.
"""
import logging
import asyncio
from datetime import time as dt_time

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    INSTAGRAM_ACCOUNTS,
    CHECK_HOUR,
    CHECK_MINUTE,
)
from instagram_checker import fetch_new_posts
from ad_checker import check_all_accounts
from state_manager import load_state, save_state, get_last_seen, update_account

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ── Nachrichten-Formatting ──────────────────────────────────────────────────

def format_post(post: dict) -> str:
    icon = "🎥" if post["is_video"] else "📸"
    caption = post["caption"].strip()
    snippet = (caption[:120] + "…") if len(caption) > 120 else caption
    return (
        f"{icon} <b>{post['account']}</b>\n"
        f"{snippet}\n"
        f"<a href='{post['url']}'>→ Post öffnen</a>"
    )


def format_ad(ad: dict) -> str:
    caption = ad["caption"].strip()
    snippet = (caption[:120] + "…") if len(caption) > 120 else caption
    text = f"📢 <b>{ad['page_name']}</b> (Anzeige)\n"
    if snippet:
        text += f"{snippet}\n"
    if ad["url"]:
        text += f"<a href='{ad['url']}'>→ Ad Library</a>"
    return text


# ── Kern-Logik ──────────────────────────────────────────────────────────────

async def run_check(app: Application):
    """Führt die vollständige Prüfung durch und sendet Ergebnisse."""
    state = load_state()
    total_new = 0

    await app.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="🔍 <b>Täglicher Instagram-Check läuft…</b>",
        parse_mode="HTML",
    )

    # 1) Neue reguläre Posts
    for account in INSTAGRAM_ACCOUNTS:
        last_shortcode = get_last_seen(state, account)
        new_posts = fetch_new_posts(account, last_shortcode)

        if new_posts:
            total_new += len(new_posts)
            header = f"✅ <b>{account}</b> — {len(new_posts)} neuer {'Post' if len(new_posts)==1 else 'Posts'}"
            await app.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=header,
                parse_mode="HTML",
            )
            for post in new_posts:
                await app.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=format_post(post),
                    parse_mode="HTML",
                    disable_web_page_preview=False,
                )
            # Neuesten Post als letzten gesehen speichern
            latest = new_posts[-1]
            update_account(state, account, latest["shortcode"], latest["timestamp"])
        else:
            logger.info(f"Keine neuen Posts: {account}")

    # 2) Aktive Anzeigen
    await app.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="📢 <b>Prüfe Meta Ad Library auf aktive Anzeigen…</b>",
        parse_mode="HTML",
    )

    ads_by_account = check_all_accounts(INSTAGRAM_ACCOUNTS)
    total_ads = sum(len(v) for v in ads_by_account.values())

    if total_ads:
        for account, ads in ads_by_account.items():
            for ad in ads:
                await app.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=format_ad(ad),
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                )
    else:
        await app.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text="Keine aktiven Anzeigen in der Ad Library gefunden.",
            parse_mode="HTML",
        )

    # Zusammenfassung
    summary = (
        f"✅ <b>Check abgeschlossen</b>\n"
        f"Neue Posts: {total_new} | Aktive Ads gefunden: {total_ads}"
    )
    await app.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=summary,
        parse_mode="HTML",
    )

    save_state(state)


# ── Bot-Commands ────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    accounts_list = "\n".join(f"• {a}" for a in INSTAGRAM_ACCOUNTS)
    await update.message.reply_html(
        f"👋 <b>Instagram Monitor Bot</b>\n\n"
        f"Überwachte Accounts:\n{accounts_list}\n\n"
        f"Täglicher Check um <b>{CHECK_HOUR:02d}:{CHECK_MINUTE:02d} Uhr</b>.\n\n"
        f"/check — Sofortiger Check\n"
        f"/status — Letzter gesehener Post je Account"
    )


async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Starte manuellen Check…")
    await run_check(context.application)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    lines = []
    for account in INSTAGRAM_ACCOUNTS:
        info = state.get(account, {})
        last_post = info.get("last_post_time", "—")
        last_check = info.get("last_checked", "—")
        lines.append(f"<b>{account}</b>\nLetzter Post: {last_post[:16]}\nGeprüft: {last_check[:16]}")
    await update.message.reply_html("\n\n".join(lines) or "Noch kein Check durchgeführt.")


# ── Startup ─────────────────────────────────────────────────────────────────

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN fehlt in .env")
    if not TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID fehlt in .env")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("check", cmd_check))
    app.add_handler(CommandHandler("status", cmd_status))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_check,
        trigger="cron",
        hour=CHECK_HOUR,
        minute=CHECK_MINUTE,
        args=[app],
        id="daily_check",
    )
    scheduler.start()

    logger.info(f"Bot gestartet — täglicher Check um {CHECK_HOUR:02d}:{CHECK_MINUTE:02d}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
