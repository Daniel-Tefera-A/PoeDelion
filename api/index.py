import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from flask import Flask, request, Response
from bot.handlers.register import register_handler

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(name)

# Define handlers as in your main.py
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/register", "/check"]]
    await update.message.reply_text(
        "👋 Welcome to the Registration Bot! \n Use buttons or commands.",
        reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/register", "/check"]]
    await update.message.reply_text(
        "Use /register to join, /check to verify \n Thank you!",
        reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Implement your check logic or keep simple response
    await update.message.reply_text("Checking registration...")

# Build the application
request = HTTPXRequest(connect_timeout=20.0, read_timeout=20.0)
application = ApplicationBuilder().token(TOKEN).request(request).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("check", check))
application.add_handler(register_handler)

@app.route("/api", methods=["POST"])
def telegram_webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, bot)
    application._process_update(update)
    return Response("ok", status=200)

if name == 'main':
    app.run()