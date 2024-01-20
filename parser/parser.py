import json

def parse_chat(filepath: str) -> bool:
    chat_file = open(filepath)

    data = json.load(chat_file)
    messages = data['messages']

    average_message_length = 0
    frequent_words = []
    frequent_emojis = []

    # parse from back to front (from newest to oldest)
    # (probably limit the number of messages to reduce parse time)
    message_count = 2500
    combined_messages = ""

    for message in reversed(messages):
        if message




    # Store data into db
        

    return True

