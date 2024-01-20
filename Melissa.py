import telebot
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I'm your girlfriend!")

@bot.message_handler(func=lambda msg: True)
def on_message(message):
    bot.send_message(message.chat.id, "Not implemented")


bot.infinity_polling()