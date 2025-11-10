# api/webhook.py   ← MUST be named webhook.py inside api/
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.request import HTTPXRequest

# Import your existing handlers
from bot.handlers.register import register_handler

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Build the app once (serverless-friendly)
request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
application = ApplicationBuilder().token(TOKEN).request(request).build()

# === Add your handlers (same as main.py + buttons + /check) ===
from bot.utils.db import load_data

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Register", "Check"]]
    reply_markup = {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": False}
    await update.message.reply_text(
        "Welcome to the Registration Bot!\n\nUse the buttons below:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use the buttons:\n"
        "• Register → Start registration\n"
        "• Check → See if you're registered"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_data()
    for entry in data:
        # Simple check: match by phone (you can improve later)
        if "phone" in entry:  # add user_id to db later if needed
            await update.message.reply_text(
                f"You're registered!\nName: {entry['name']}\nPhone: {entry['phone']}"
            )
            return
    await update.message.reply_text("Not registered yet. Use 'Register' button!")

# Add all handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("check", check))
application.add_handler(MessageHandler(filters.Regex("^Register$"), start_registration))  # button
application.add_handler(MessageHandler(filters.Regex("^Check$"), check))                # button
application.add_handler(register_handler)

# === Vercel handler (THIS IS THE ONLY THING Vercel calls) ===
def handler(event, context=None):
    """Vercel serverless function"""
    try:
        update = Update.de_json(event["body"], application.bot)
        application.process_update(update)
    except Exception as e:
        print("Error:", e)
    return {
        "statusCode": 200,
        "body": "OK"
    }

# This is what Vercel expects
export default handler