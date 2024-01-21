from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.create import Models
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

def create_user_to_database(
        userId, 
        state,
):
    db_url = DB_URL
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # check if userid alr in database
    criteria = {"userId": "1"}
    existing_row = session.query(Models).filter_by(**criteria).first()
    if existing_row:
        session.delete(existing_row)
        session.commit()

    new_user = Models(
        userId=userId, 
        currentState=state,
    )

    try:
        session.add(new_user)
        session.commit()
        print(f"New User {userId} has been added to Models Table")
    except Exception as e:
        # Handle any exceptions or errors that may occur during the operation
        print(f"Error adding new user: {e}")
        session.rollback()
    finally:
        # Close the session
        session.close()

def initialize_user_to_database(
        userId, 
        personalityName, 
        age, 
        gender, 
        race
):
    db_url = DB_URL
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = Models(
        userId=userId, 
        personalityName=personalityName,
        age=age, 
        gender=gender, 
        race=race, 
        brief_description=""
    )

    try:
        session.add(new_user)
        session.commit()
        print(f"New User {userId} for personality {personalityName} data added to Models Table")
    except Exception as e:
        # Handle any exceptions or errors that may occur during the operation
        print(f"Error adding new user: {e}")
        session.rollback()
    finally:
        # Close the session
        session.close()



# initialize_user_to_database(
#     userId="Victor", 
#     age=20, 
#     gender="Male", 
#     race="Chinese", 
#     brief_description="Big Coder", 
# )
    # average_message_length=5, 
    #frequent_words=["LOL", "HAHA"],
    # frequent_emojis=["smiley"], 
    # first_letter_capped=True, 
    # summary="Hello this is a summary", 
    # message_history=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": "Who won the world series in 2020?"},
    #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #     {"role": "user", "content": "Where was it played?"}
    # ]