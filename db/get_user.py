from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.create import Models
import json

def get_user_from_database(userId):
    db_url = "postgresql://victorlai:@localhost:5432/melissa"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(Models).filter_by(userId=str(userId)).first()

    if user is not None:
        print(f"User found: {user.userId}")
    else:
        print("User not found.")

    user_json = {
        "userId": user.userId, 
        "personalityName": user.personalityName,
        "average_message_length": user.average_message_length,
        "frequent_words": user.frequent_words,
        "age": user.age, 
        "gender": user.gender, 
        "race": user.race, 
        "brief_description": user.brief_description, 
        "frequent_emojis": user.frequent_emojis, 
        "first_letter_capped": user.first_letter_capped, 
        "summary": user.summary, 
        "message_history": user.message_history, 
        "past_messages": user.past_messages,
        "current_state": user.currentState
    }

    return user_json

# print(get_user_from_database("204593709_969802785"))