from typing import Any, List
from openai import OpenAI
from dotenv import load_dotenv
import os
from db.update_user import update_user_summary_message_history

load_dotenv()

# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
client = OpenAI()

def create_prompt(personality):
    nl = "\n"
    stats = f"""You are pretending to message me as a persona, with these following traits. 
    You are a {personality['gender']} with age {personality['age']}. Your name is {personality['personalityName']}.
    You are a Singaporean and your race is {personality['race']}.
    Respond with an average of {personality['average_message_length']} words. 
    Your text messages {"do" if personality['first_letter_capped'] else "do not"} start with a capital letter.
    Your frequently used words include {', '.join(personality['frequent_words'])}, use them at the frequency of the example conversations
    Your frequently used emojis include {', '.join(personality['frequent_emojis'])}, use them at the frequency of the example conversation.
    Here is some examples of our past conversations, try to mimic this personality as much as possible:
    {nl.join(personality['past_messages'])}
    """
    summary = ("Here is a summary of past text events for your information, I may ask you about them to check if you forget: " + personality['summary']) if personality['summary'] else ""
    return stats + "\n" + summary

def get_response(userId: str, prompt: str, message_history: List[Any]) -> str:
    print(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            *message_history
        ],
        max_tokens=100
    )

    response_message = response.choices[0].message.content
    print(message_history)
    new_message_history = message_history + [{"role": "assistant", "content": response_message}]
    
    # Once every x, make a summary of the message history and add it to the prompt in db
    if len(message_history) > 10:
        update_user_summary_message_history(userId=userId, summary=get_summary(new_message_history), message_history=[])
    else:
        update_user_summary_message_history(userId=userId, message_history=new_message_history)
    print(f"New message history: {new_message_history}")
    

    return response_message

def get_summary(message_history):
    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_history])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please help me summarize the following conversation in 3 sentences:\\n{conversation}"},
        ],
        max_tokens=100
    )

    summary = response.choices[0].message.content

    return summary