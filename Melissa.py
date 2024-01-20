import telebot
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

initialisation_stage = 0

@bot.message_handler(func=lambda msg: True)
def on_message(message):
    if initialisation_stage == 1:
        bot.send_message(message.chat.id, "")
    bot.send_message(message.chat.id, "Not implemented")

@bot.message_handler(content_types=['document','video','voice','contact','photo'])
def handle_file(message):
    if initialisation_stage != 0:
        bot.send_message(message.chat.id, "This bot does not support non-text messages.")
        return
    bot.send_message(message.chat.id, "File received!")
    filetype = message.document.mime_type
    if filetype != "application/json":
        bot.send_message(message.chat.id, "Incorrect file format!")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        with open("chat_history.json", "wb") as file:
            file.write(downloaded_file)
        bot.send_message(message.chat.id, "Chat history received! Now, would you like me to be male or female?")
        # TODO
        initialisation_stage += 1
    except:
        bot.send_message(message.chat.id, "Oops! Something went wrong. Please try again.")
    
'''
Interrogation process (stuff that can't be inferred from chat history easily)
1. Age
2. Gender
3. Race
4. Nationality
5. Brief description of the person (not more than 30 words)
'''

@bot.message_handler(commands=['start'])
def initialise_girlfriend(message):
    if initialisation_stage != 0:
        bot.send_message("You've already started a conversation with me!")
        return
    bot.send_message(message.chat.id, "Hello! Send me a .json file from your chat history to initialise me.")
    

bot.infinity_polling()