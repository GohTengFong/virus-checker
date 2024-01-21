from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db.create import Models
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

def update_user_stats(
        userId, 
        personalityName=None, 
        age=None, 
        gender=None, 
        race=None,
        current_state=None
):
    db_url = DB_URL
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(Models).filter_by(userId=str(userId)).first()

        if user:
            user.personalityName = personalityName
            user.age = age
            user.gender = gender
            user.race = race
            user.currentState = current_state if current_state is not None else user.currentState
            session.commit()
            print(f"Uploaded chat info for user {user.userId}")
        else:
            print(f"User {user.userId} not found")
    except Exception as e:
        session.rollback()
        print(f"Error updating user chat info: {str(e)}")
    finally:
        session.close()

def update_user_chat_info(
        userId, 
        average_message_length, 
        frequent_words, 
        frequent_emojis, 
        first_letter_capped, 
        example_text,
        # summary, 
        # message_history
        ):
    db_url = DB_URL
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(Models).filter_by(userId=str(userId)).first()

        if user:
            user.average_message_length = average_message_length
            user.frequent_words = frequent_words
            user.frequent_emojis = frequent_emojis
            user.first_letter_capped = first_letter_capped
            user.past_messages = example_text
            # user.summary = summary
            # user.message_history = message_history
            session.commit()
            print(f"Uploaded chat info for user {user.userId}")
        else:
            print(f"User {user.userId} not found")
    except Exception as e:
        session.rollback()
        print(f"Error updating user chat info: {str(e)}")
    finally:
        session.close()

def update_user_summary_message_history(userId, summary: Optional[any] = None, message_history: Optional[any] = None):
    db_url = DB_URL
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(Models).filter_by(userId=str(userId)).first()

        if user:
            if summary is not None:
                user.summary = user.summary + summary if user.summary else summary
            if message_history is not None:
                user.message_history = message_history
            session.commit()
            print(f"Update summary and message history for user {user.userId}")
        else:
            print(f"User {user.userId} not found")
    except Exception as e:
        session.rollback()
        print(f"Error updating summary: {str(e)}")
    finally:
        session.close()


# update_user_chat_info(
#     userId="Victor",
#     average_message_length=5, 
#     frequent_words=["LOL", "HAHA"],
#     frequent_emojis=["smiley"], 
#     first_letter_capped=True, 
#     summary="Hello this is a summary", 
#     message_history=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )

# update_user_summary("Victor", "This is a new updated summary.", [
#         {"role": "system", "content": "This is an edit."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ])