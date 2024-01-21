import json
from collections import Counter
from emoji import UNICODE_EMOJI
from typing import Tuple
from db.update_user import update_user_chat_info

common_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'u', 'ur']

def parse_chat(userId: str, filepath: str) -> bool:
    data = None
    with open(filepath, encoding="utf8") as chat_file:
        data = json.load(chat_file)

        if 'type' not in data and data['type'] != 'personal_chat':
            return False, 0

    messages = data['messages']
    personality_id = data['id']
    from_id = "user" + str(personality_id)

    average_message_length = 0
    frequent_words = []
    frequent_emojis = []
    first_letter_capped = False

    # parse from back to front (from newest to oldest)
    # (probably limit the number of messages to reduce parse time)
    message_count = 0
    message_max = 10000

    example_text = []
    example_text_max = 100
    example_text_used = 0
    
    combined_words = ""
    combined_messages_words = []
    combined_messages_emojis = []
    total_valid_messages = 0
    total_valid_words = 0
    first_letter_capped_count = 0

    for message in reversed(messages):
        message_content = message['text']
        if example_text_used == example_text_max:
            break
        if 'from_id' not in message:
            continue
        if len(message_content) > 0 and isinstance(message_content, str):
            if message['from_id'] == from_id:
                # from the other person
                example_text.append(f"assistant: {message_content}")
            else:
                # from me
                example_text.append(f"user: {message_content}")
            example_text_used += 1

    for message in reversed(messages):
        message_content = message['text']
        if message_count == message_max:
            break
            
        if 'from_id' not in message:
            continue
        if message['from_id'] != from_id:
            continue

        # only count use messages from personality
        if len(message_content) > 0 and isinstance(message_content, str):
            if message_content[0].islower():
                first_letter_capped_count += 1
            elif message_content[0].isupper():
                first_letter_capped_count -= 1

            # ignore outliers (more than 100 words in 1 message)
            message_content_words = message_content.split()
            if len(message_content_words) < 100:
                total_valid_messages += 1
                total_valid_words += len(message_content_words)

                combined_words += message_content

                # for word in message_content_words:
                #     if word in UNICODE_EMOJI:
                #         print(word)
                #         combined_messages_emojis += [UNICODE_EMOJI[word]]
                #     else:
                #         combined_messages_words += [word]

            message_count += 1
        
    average_message_length = total_valid_words / total_valid_messages
    first_letter_capped = first_letter_capped_count < 0

    combined_messages_emojis = [char for char in combined_words if char in UNICODE_EMOJI['en']]
    combined_messages_words = ''.join([char for char in combined_words if char not in UNICODE_EMOJI['en']]).split()
    combined_messages_words_filtered = list(filter(lambda x: x.lower() not in common_words, combined_messages_words))

    frequent_words = list(map(lambda x: x[0], Counter(combined_messages_words_filtered).most_common(10)))
    frequent_emojis = list(map(lambda x: x[0], Counter(combined_messages_emojis).most_common(10)))

    # Store data into db
    update_user_chat_info(f"{userId}", average_message_length, frequent_words, frequent_emojis, first_letter_capped, example_text)

    return True

# def get_example_text(userId: str, filepath: str) -> bool:
#     data = None
#     with open(filepath, encoding="utf8") as chat_file:
#         data = json.load(chat_file)
#         if 'type' not in data and data['type'] != 'personal_chat':
#             return False, 0

#     messages = data['messages']
#     personality_id = data['id']
#     from_id = "user" + str(personality_id)
    
#     message_count = 0
#     # take and format the most recent 100 messages
    
#     return example_text