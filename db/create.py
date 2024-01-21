from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.types import Boolean
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Models(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String, unique=True, nullable=False)
    personalityName = Column(String, nullable=True)
    average_message_length = Column(Integer)
    frequent_words = Column(ARRAY(String))
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    race = Column(String, nullable=True)
    brief_description = Column(Text, nullable=True)
    frequent_emojis = Column(ARRAY(String), nullable=True)
    first_letter_capped = Column(Boolean, default=0)
    summary = Column(Text, nullable=True)
    message_history = Column(JSONB, nullable=True)
    past_messages = Column(ARRAY(Text))
    currentState = Column(Integer, nullable=False)

Base.metadata.create_all(engine)



