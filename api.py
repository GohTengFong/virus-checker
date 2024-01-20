from typing import Any, List
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI()
load_dotenv()

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

def get_response(prompt: str, message_history: List[Any]) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            message_history
        ],
        max_tokens=100
    )

    response_message = response.choices[0].message
    new_message_history = message_history + [response_message]
    # Once every x, make a summary of the message history and add it to the prompt in db

    return response_message

    