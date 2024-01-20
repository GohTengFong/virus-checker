import telebot
from dotenv import load_dotenv
import os
import requests
from langchain_community.llms import HuggingFaceHub

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
VIRUS_TOTAL_URL = os.getenv("VIRUS_TOTAL_URL")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")

'''
@bot.message_handler(func=lambda msg: True)
def on_message(message):
    bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")
'''

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

class LLM:
  def __init__(self):
    model_string = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    self.chat = []
    self.llm = HuggingFaceHub(repo_id=model_string, model_kwargs={"temperature": 0.5, "max_length":64,"max_new_tokens":512})

  def get_reply(self, instruction):
    reply = self.llm.invoke(instruction)
    return reply

llm = LLM()

'''
@bot.message_handler(func=lambda msg: True)
def on_message(message):
    print(f"Message received! {message}")
    reply = llm.get_reply(message.text)
    bot.reply_to(message, reply)
'''
    
bot.infinity_polling()