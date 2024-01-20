import telebot
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")
VIRUS_TOTAL_UPLOAD_URL = os.getenv("VIRUS_TOTAL_UPLOAD_URL")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Upload a file and I will check it for malware!")

@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("received_documents.pdf", "wb") as file:
        file.write(downloaded_file)

    bot.reply_to(message, "I have received your file! Please wait while I perform my checks!")

    files = {"file": ("received_documents.pdf", open("received_documents.pdf", "rb"), "application/pdf")}
    analysis_url = upload_file(get_upload_url(), files)

    analysis = get_analysis(analysis_url)
    
def get_upload_url():
    """
    Returns the URL to upload the file to.

    Returns:
        str: The URL to upload the file to.
    """

    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY,
    }

    response = requests.get(VIRUS_TOTAL_UPLOAD_URL, headers=headers)
    upload_url = json.loads(response.text)["data"]
    
    return upload_url

def upload_file(upload_url, files):
    """
    Uploads the file to VirusTotal.

    Args:
        upload_url (str): The URL to upload the file to.
        files (file): The file to upload.

    Returns
        str: The URL to obtain the analysis.
    """
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY,
    }

    response = requests.post(upload_url, files=files, headers=headers)
    analysis_url = json.loads(response.text)["data"]["links"]["self"]
    
    return analysis_url

def get_analysis(analysis_url):
        """
        Returns the analysis.

        Args:
            analysis_url (str): The URL to obtain the analysis.

        Returns:
            dict: The analysis as a Python dictionary.
        """
        headers = {
            "accept": "application/json",
            "x-apikey": VIRUS_TOTAL_API_KEY,
        }

        response = requests.get(analysis_url, headers=headers)
        analysis = json.loads(response.text)

        return analysis

bot.infinity_polling()