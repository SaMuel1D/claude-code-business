import logging
import os
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from google_services import (
    get_today_events,
    get_urgent_mails,
    get_unread_mails,
    get_week_events,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ALLOWED_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])


def authorized(update: Update) -> bool:
    return update.effective_chat.id == ALLOWED_CHAT_ID


def format_event(event: dict) -> str:
    start = event["start"].get("dateTime", event["start"].get("date", ""))
    if "T" in start:
        time_str = datetime.fromisoformat(start).strftime("%H:%M")
    else:
        time_str = "ganztags"
    return f"• {time_str} — {event.get('summary', '(kein Titel)')}"


def format_mail(mail: dict) -> str:
    return f"📨 *{mail['from']}*\n_{mail['subject']}_"


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    await update.message.reply_text(
        "Hallo! Dein persönlicher Kalender- & Mail-Bot.\n\n"
        "/heute — Termine heute\n"
        "/woche — Termine diese Woche\n"
        "/mails — Ungelesene Mails (max. 5)\n"
        "/dringend — Dringende Mails"
    )


async def cmd_heute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    try:
        events = get_today_events()
        if not events:
            await update.message.reply_text("Heute keine Termine. 🎉")
            return
        lines = ["📅 *Heute:*\n"] + [format_event(e) for e in events]
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        logger.error("Fehler /heute: %s", e)
        await update.message.reply_text(f"Fehler: {e}")


async def cmd_woche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    try:
        events = get_week_events()
        if not events:
            await update.message.reply_text("Diese Woche keine Termine.")
            return
        lines = ["📅 *Diese Woche:*\n"]
        current_day = None
        for e in events:
            start = e["start"].get("dateTime", e["start"].get("date", ""))
            dt = datetime.fromisoformat(start.split("T")[0])
            day = dt.strftime("%A, %d.%m.")
            if day != current_day:
                lines.append(f"\n*{day}*")
                current_day = day
            lines.append(format_event(e))
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        logger.error("Fehler /woche: %s", e)
        await update.message.reply_text(f"Fehler: {e}")


async def cmd_mails(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    try:
        mails = get_unread_mails(max_results=5)
        if not mails:
            await update.message.reply_text("Keine ungelesenen Mails. 📭")
            return
        lines = ["📬 *Ungelesene Mails:*\n"] + [format_mail(m) for m in mails]
        await update.message.reply_text("\n\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        logger.error("Fehler /mails: %s", e)
        await update.message.reply_text(f"Fehler: {e}")


async def cmd_dringend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not authorized(update):
        return
    try:
        mails = get_urgent_mails()
        if not mails:
            await update.message.reply_text("Keine dringenden Mails. ✅")
            return
        lines = ["🚨 *Dringende Mails:*\n"] + [format_mail(m) for m in mails]
        await update.message.reply_text("\n\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        logger.error("Fehler /dringend: %s", e)
        await update.message.reply_text(f"Fehler: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("heute", cmd_heute))
    app.add_handler(CommandHandler("woche", cmd_woche))
    app.add_handler(CommandHandler("mails", cmd_mails))
    app.add_handler(CommandHandler("dringend", cmd_dringend))
    logger.info("Bot läuft...")
    app.run_polling()


if __name__ == "__main__":
    main()
