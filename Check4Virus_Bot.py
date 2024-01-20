import telebot
from dotenv import load_dotenv
import os
import json
import requests
from langchain_community.llms import HuggingFaceHub

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
VIRUS_TOTAL_UPLOAD_URL = os.getenv("VIRUS_TOTAL_UPLOAD_URL")
bot = telebot.TeleBot(BOT_TOKEN)

class LLM:
  def __init__(self):
    model_string = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    self.chat = []
    self.llm = HuggingFaceHub(repo_id=model_string, model_kwargs={"temperature": 0.5, "max_length":64,"max_new_tokens":512})

  def get_reply(self, instruction):
    reply = self.llm.invoke(instruction)
    return reply

llm = LLM()

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")


@bot.message_handler(func=lambda msg: True)
def on_message(message):
    bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")


@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("received_documents.pdf", "wb") as file:
        file.write(downloaded_file)

    bot.reply_to(message, "I have received your file! Please wait while I perform my checks!")
    files = {"file": ("received_documents.pdf", open("received_documents.pdf", "rb"), "application/pdf")}
    bot.send_message(message.chat.id, "Uploading file to VirusTotal...")
    analysis_url = upload_file(get_upload_url(), files)
    analysis = get_analysis(analysis_url)
    bot.send_message(message.chat.id, "Waiting for VirusTotal to finish analysis...")
    while analysis['data']['attributes']['status'] == 'queued':
       print("obtaining analysis")
       analysis = get_analysis(analysis_url)
    analysis_string = str(analysis)
    bot.send_messsage(message.chat.id, "Obtaining summary from AI...")
    prompt = f"Analyse the following VirusTotal file report: {analysis_string} Tell me, within 300 words, whether it is malicious or not, and why."
    llm_response = llm.get_reply(prompt)
    bot.send_message(message.chat.id, analysis_string)       
    
# Generates a URL from VirusTotal to upload file to
def get_upload_url():
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY,
    }

    response = requests.get(VIRUS_TOTAL_UPLOAD_URL, headers=headers)
    upload_url = json.loads(response.text)["data"]
    
    return upload_url

# Uploads the file to VirusTotal, and returns the URL to obtain the analysis.
def upload_file(upload_url, files):
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY,
    }

    response = requests.post(upload_url, files=files, headers=headers)
    analysis_url = json.loads(response.text)["data"]["links"]["self"]
    
    return analysis_url

# Returns the analysis as a Python dictionary
def get_analysis(analysis_url):
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY,
    }

    response = requests.get(analysis_url, headers=headers)
    analysis = json.loads(response.text)

    return analysis

bot.infinity_polling()