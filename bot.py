"""Prebunk - Telegram front door (Track 1).

Receives a message the user deliberately forwards, sends it to analyze_message(),
always replies to the user, and forwards low-confidence cases to a human
reviewer group (REVIEWER_CHAT_ID).
"""
import logging
import os

from dotenv import load_dotenv
from langfuse import get_client
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from agent import analyze_message  # the real agent (Step 4)

load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
REVIEWER_CHAT_ID = os.getenv("REVIEWER_CHAT_ID", "").strip()

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)  # httpx logs URLs that contain the bot token
log = logging.getLogger("prebunk.bot")

MAX_LEN = 4000  # Telegram allows 4096 characters per message

WELCOME = (
    "Hi, I'm Prebunk.\n\n"
    "Forward me a message you're unsure about. I'll explain which persuasion or "
    "manipulation techniques it might be using, and check any factual claim I can.\n\n"
    "I only see messages you send me directly. I don't judge whether an opinion is "
    "right or wrong - only how a message tries to move you, and whether its facts hold up."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(WELCOME)


async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Helper: send /chatid in any chat (including the reviewer group) to see its ID."""
    await update.effective_message.reply_text(f"This chat's ID is: {update.effective_chat.id}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    text = (msg.text or msg.caption or "").strip()  # caption = text attached to a forwarded photo

    if not text:
        await msg.reply_text("I can only check text messages right now - try forwarding one with words in it.")
        return

    log.info("Analyzing a message (%d characters)", len(text))  # length only, never the content
    await msg.reply_text("Checking this message - it usually takes 15-30 seconds...")
    await context.bot.send_chat_action(chat_id=msg.chat_id, action="typing")

    try:
        result = await analyze_message(text)
    except Exception:
        log.exception("analyze_message failed")
        await msg.reply_text("Sorry, something went wrong while checking that message. Please try again in a minute.")
        return

    await msg.reply_text(result.get("reply", "")[:MAX_LEN] or "I couldn't produce an answer for that one.")

    if result.get("escalate"):
        await escalate(context, text, result)


async def escalate(context: ContextTypes.DEFAULT_TYPE, original: str, result: dict) -> None:
    if not REVIEWER_CHAT_ID:
        log.warning("Escalation requested but REVIEWER_CHAT_ID is not set in .env")
        return

    note = (
        "FLAGGED FOR HUMAN REVIEW\n\n"
        f"Reason: {result.get('escalation_note') or 'not given'}\n\n"
        f"Original message:\n{original}\n\n"
        f"Reply the user received:\n{result.get('reply', '')}"
    )
    try:
        await context.bot.send_message(chat_id=int(REVIEWER_CHAT_ID), text=note[:MAX_LEN])
        log.info("Escalated to reviewer group")
    except Exception:
        log.exception("Could not send to reviewer group - check REVIEWER_CHAT_ID and that the bot is in the group")


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chatid", chat_id))
    # Only analyze private chats - the bot never reads conversations in groups.
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, handle_message))

    log.info("Prebunk bot is running. Press Ctrl+C to stop.")
    app.run_polling()
    get_client().flush()  # send any remaining traces to Langfuse on shutdown


if __name__ == "__main__":
    main()
