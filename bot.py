import telebot
from dotenv import load_dotenv
import os
import requests

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
    
    @bot.message_handler(content_types=['document'])
    def handle_pdf(message):
        if message.document.mime_type == 'application/pdf':
            file_info = bot.get_file(message.document.file_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

            with open("temp.pdf", "wb") as file:
                file.write(requests.get(file_url).content)
        
            with open("temp.pdf", "rb") as file:
                bot.send_document(message.chat.id, file)

            bot.reply_to(message, "Received your PDF File.")
            
        else:
            bot.reply_to(message, "Please send a valid PDF File.")
                                     
    return bot

bot = init_bot()
bot.infinity_polling()