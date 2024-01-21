import telebot
from telebot import types
from dotenv import load_dotenv
from enum import Enum
import os
import json
import requests
from db.add_user import create_user_to_database
from db.update_user import update_user_stats
from db.get_user import get_user_from_database
from parse import parse_chat
from api import get_response, create_prompt

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

class Init_Stage():
    GENDER_STAGE = 0
    RACE_STAGE = 1
    AGE_STAGE = 2
    JSON_STAGE = 3
    COMPLETED_STAGE = 4

# gender = "X"
# race = "X"
# age = 69
# desc = "X"
# name = "X"

user_data = {}


'''
Interrogation process (stuff that can't be inferred from chat history easily)
1. Gender
2. Race
3. Age
4. Brief description of the person (not more than 30 words)
'''

def refresh_state(message):
    if bot.get_state(message.chat.id) is None:
        user = get_user_from_database(message.chat.id)
        bot.set_state(message.chat.id, user['current_state'])

@bot.message_handler(commands=['start'])
def initialise_girlfriend(message):
    # global curr_stage
    # if curr_stage != Init_Stage.JSON_STAGE:
    #     bot.send_message(message.chat.id, "You've already started a conversation with me!")
    #     return
    create_user_to_database(message.chat.id, Init_Stage.GENDER_STAGE)
    refresh_state(message)
    bot.set_state(message.chat.id, Init_Stage.GENDER_STAGE)
    ask_gender(message.chat.id)

@bot.message_handler(func=lambda msg: True)
def on_message(message):
    # global gender
    # global race
    # global age
    # global desc
    # global name
    # global user_data
    refresh_state(message)
    curr_stage = bot.get_state(message.chat.id)
    user_id = message.chat.id

    if curr_stage == Init_Stage.JSON_STAGE:
        ask_json(message.chat.id)
    elif curr_stage == Init_Stage.GENDER_STAGE:
        gender_response = message.text
        if gender_response == "Male" or gender_response == "Female":
            gender = gender_response
            # user_data[user_id] = {}
            # user_data[user_id]["gender"] = gender
            update_user_stats(f"{message.chat.id}", gender=gender, current_state=Init_Stage.RACE_STAGE)
            bot.set_state(message.chat.id, Init_Stage.RACE_STAGE)
            ask_race(message.chat.id)
        else:
            ask_gender(message.chat.id)
    elif curr_stage == Init_Stage.RACE_STAGE:
        race_response = message.text
        if race_response == "Chinese" or race_response == "Malay" or race_response == "Indian" or race_response == "Eurasian":
            race = race_response
            # user_data[user_id]["race"] = race
            update_user_stats(f"{message.chat.id}", race=race, current_state=Init_Stage.AGE_STAGE)
            bot.set_state(message.chat.id, Init_Stage.AGE_STAGE)
            ask_age(message.chat.id)
        else:
            ask_race(message.chat.id)
    elif curr_stage == Init_Stage.AGE_STAGE:
        age_response = message.text
        if not age_response.isnumeric():
            ask_age(message.chat.id)
        else:
            age_response = int(age_response)
            if age_response < 0 or age_response > 100:
                bot.send_message(message.chat.id, "Please enter a valid age.")
            else:
                age = age_response
                # user_data[user_id]["age"] = age
                update_user_stats(f"{message.chat.id}", age=age, current_state=Init_Stage.JSON_STAGE)
                bot.set_state(message.chat.id, Init_Stage.JSON_STAGE)
                ask_json(message.chat.id)

    elif curr_stage == Init_Stage.COMPLETED_STAGE:
        # Interact with AI here
        personality = get_user_from_database(message.chat.id)
        print(personality)

        prompt = create_prompt(personality)
        message_history = (personality["message_history"] if personality["message_history"] else []) + [{"role": "user", "content": message.text}]
        print(message_history)
        response_message = get_response(message.chat.id, prompt, message_history)
        bot.send_message(message.chat.id, response_message)
    else:
        bot.send_message(message.chat.id, "Error!")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    refresh_state(message)
    curr_stage = bot.get_state(message.chat.id)
    user_id = message.chat.id
    # global name
    if curr_stage != Init_Stage.JSON_STAGE:
        bot.send_message(message.chat.id, "This bot does not support non-text messages.")
        return
    bot.send_message(message.chat.id, "File received! Please wait while we process the data...")
    filetype = message.document.mime_type
    if filetype != "application/json":
        bot.send_message(message.chat.id, "Incorrect file format!")
        return
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        with open(f"/tmp/{message.chat.id}.json", "wb") as file:
            file.write(downloaded_file)
        with open(f"/tmp/{message.chat.id}.json", "r") as file:
            data = json.load(file)
            personality_id = data['id']
            personality_name = data['name']
            update_user_stats(f"{message.chat.id}", personalityName=personality_name)

        success = parse_chat(message.chat.id, f"/tmp/{message.chat.id}.json")
        if not success:
            bot.send_message(message.chat.id, "Invalid file format. Please resend the correct file!")
            return
             
        update_user_stats(f"{message.chat.id}", current_state=Init_Stage.COMPLETED_STAGE)
        bot.set_state(message.chat.id, Init_Stage.COMPLETED_STAGE)
        bot.send_message(message.chat.id, "You have now completed the AI initialisation.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Oops! Something went wrong. Please try again. {str(e)}")
        
def ask_json(id):
    bot.send_message(id, "Hello! Send me a .json file from your chat history to initialise me.")

def ask_gender(id):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Male')
    button2 = types.KeyboardButton('Female')
    keyboard.add(button1, button2)
    bot.send_message(id, "What gender would you like me to be?", reply_markup=keyboard)

def ask_race(id):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('Chinese')
    button2 = types.KeyboardButton('Malay')
    button3 = types.KeyboardButton('Indian')
    button4 = types.KeyboardButton('Eurasian')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(id, "What race would you like me to be?", reply_markup=keyboard)

def ask_age(id):
    bot.send_message(id, "What age would you like me to be?")

def ask_description(id):
    bot.send_message(id, "Within 30 words, give me a brief description of my personality.")

bot.infinity_polling()