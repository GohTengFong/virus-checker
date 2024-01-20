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
    bot.send_message(message.chat.id, "Hello! I'm your girlfriend! Send me a .json file from your chat history to initialise me.")

@bot.message_handler(func=lambda msg: True)
def on_message(message):
    bot.send_message(message.chat.id, "Not implemented")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    bot.send_message(message.chat.id, "File received!")
    filetype = message.document.mime_type
    if filetype != "application/json":
        bot.send_message(message.chat.id, "Incorrect file format!")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        with open("chat_history.pdf", "wb") as file:
            file.write(downloaded_file)
        bot.send_message(message.chat.id, "Chat history received!")
    except:
        bot.send_message(message.chat.id, "Oops! Something went wrong.")
    

bot.infinity_polling()