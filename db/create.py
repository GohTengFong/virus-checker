from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import LONGTEXT, JSONB, ARRAY
from sqlalchemy.types import Boolean

db_url = " postgresql://victorlai:@localhost:5432/melissa"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Models(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    average_message_length = Column(Integer)
    frequent_words = Column(ARRAY(String))
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    race = Column(String, nullable=True)
    brief_description = Column(LONGTEXT, nullable=True)
    frequent_emojis = Column(String, nullable=True)
    first_letter_capped = Column(Boolean, default=0)
    summary = Column(LONGTEXT, nullable=True)
    message_history = Column(JSONB, nullable=True)

Base.metadata.create_all(engine)



