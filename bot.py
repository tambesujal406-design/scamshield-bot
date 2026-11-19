"""ScamShield bot: forward or paste a suspicious message, get a 0-100 risk score."""
import logging
import os

from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      LinkPreviewOptions, Update)
from telegram.constants import ParseMode
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler, filters)

from formatting import format_reply
from scorer import analyze

load_dotenv()
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    level=logging.INFO)
# httpx logs every request URL, and Telegram URLs contain your bot token
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("scamshield")

REPORT_BUTTON = InlineKeyboardButton("Report scam", url="https://cybercrime.gov.in")
HELP_TEXT = (
    "Forward or paste any suspicious message and I'll give it a 0-100 risk score "
    "with the reasons.\n\n"
    "Privacy: I don't save your messages. Only the score is logged.\n"
    "Limits: this is a rule-based check. It can miss new scams or flag safe "
    "messages, so treat it as a second opinion."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(HELP_TEXT)


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    text = msg.text or msg.caption or ""
    if not text.strip():
        await msg.reply_text("I can only check text for now. Paste or forward the message text.")
        return

    result = analyze(text)
    log.info("scored=%s level=%s", result.score, result.level)  # never log the message itself

    keyboard = InlineKeyboardMarkup([[
        REPORT_BUTTON,
        InlineKeyboardButton("Correct", callback_data="fb:yes"),
        InlineKeyboardButton("Wrong", callback_data="fb:no"),
    ]])
    await msg.reply_text(
        format_reply(result),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer("Thanks for the feedback!")
    log.info("feedback=%s", query.data)
    # remove the feedback buttons so people can't vote twice
    await query.edit_message_reply_markup(InlineKeyboardMarkup([[REPORT_BUTTON]]))


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("BOT_TOKEN is missing. Copy .env.example to .env and paste your token.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(CallbackQueryHandler(feedback, pattern=r"^fb:"))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, check_message))

    log.info("ScamShield is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
