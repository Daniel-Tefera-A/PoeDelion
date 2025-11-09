import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from bot.handlers.register import register_handler
from telegram import ReplyKeyboardMarkup
from  bot.utils.db import load_data

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    user_name = user.first_name
    found_entries = [entry for entry in data if entry["name"] == user_name]
    if found_entries: 
        entries_text = "".join([f'Name: {e["name"]}, Phone: {e["phone"]}' for e in found_entries])
        await update.message.reply_text(f"You are registered: {entries_text}")
    else:
        await update.message.reply_text("You are not registered yet. Use /regiser to register")

    

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/register", "/check"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Welcome to the Registration Bot!\n\nUse the buttons below to register or check your info", reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/reister", "/check"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome! This is a simple registration bot!\n"
        "Use the buttons or these commands:\n"
        "/start - Restart the bot.\n"
        "/register - Enter your information and join.\n"
        "/check - Check your information if you have registred.\n "
        "Thank you for using our bot!😊"
    )

def main():
    request = HTTPXRequest(connect_timeout=20.0, read_timeout=20.0)
    app = ApplicationBuilder().token(TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(register_handler)



    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()



