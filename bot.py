import telebot
from dotenv import load_dotenv
import os

load_dotenv()

def init_bot():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['start'])
    def on_start(message):
        bot.send_message(message.chat.id, "Beep, boop, starting bot...")

    @bot.message_handler(func=lambda msg: True)
    def on_message(message):
        bot.reply_to(message, message.text)

    return bot

bot = init_bot()
bot.infinity_polling()