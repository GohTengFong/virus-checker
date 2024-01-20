import telebot
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def init_bot():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
    VIRUS_TOTAL_URL = os.getenv("VIRUS_TOTAL_URL")
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")
    
    @bot.message_handler(content_types=['document'])
    def handle_pdf(message):
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        bot.reply_to(message, "I have received your file! Please wait while I perform my checks!")
        
        with open("temp.pdf", "wb") as file:
            file.write(requests.get(file_url).content)

        response = None

        with open("temp.pdf", "rb") as file:
            response = check_file(file)

        bot.send_message(message.chat.id, response)        

    def check_file(file):
        headers = {
            "accept": "application/json",
            "content-type": "multipart/form-data",
            "file": file,
            "x-apikey": VIRUS_TOTAL_API_KEY,
        }

        response = requests.get(VIRUS_TOTAL_URL, headers=headers)
        
        return response
                                     
    return bot

bot = init_bot()
bot.infinity_polling()