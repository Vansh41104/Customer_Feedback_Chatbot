import sys
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Column, Integer, Boolean, Numeric, Text, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Tell me a joke about france",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
#
# print(chat_completion.choices[0].message.content)
#
# sys.exit()

# create an engine
engine = create_engine("postgresql+psycopg2://admin:password@localhost/kanari_insights")

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


class Base(DeclarativeBase):
    pass


class Feedback(Base):
    __tablename__ = "chatbot_data"
    id = Column(Integer, primary_key=True)
    customer_id = Column('customer_id', Integer)
    translated_comment = Column('translated_comment', Text)
    agent_name = Column('agent_name', String(256))
    brand_name = Column('brand_name', String(256))
    outlet_location = Column('outlet_location', String(256))
    feedback_date = Column('feedback_date', Date)
    promoter = Column('promoter', Boolean)
    detractor = Column('detractor', Boolean)
    passive = Column('passive', Boolean)


feedbacks = session.query(Feedback).filter(Feedback.translated_comment != '').all()

# 4 - print movies' details
print('\n### All movies:')
for feedback in feedbacks:
    print(f'{feedback.translated_comment}')
print('')

# Define the start and end dates for January 2024
start_date = date(2024, 1, 1)
end_date = date(2024, 1, 10)

# Iterate over each day in January
current_date = start_date
while current_date < end_date:
    # Query for feedback from the current day
    feedbacks = session.query(Feedback).filter(
        Feedback.feedback_date == current_date,
        Feedback.translated_comment != ''
    ).all()

    feedback_string = "\n".join([feedback.translated_comment for feedback in feedbacks])

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Summarise the following content: " + feedback_string,
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(f"\nFeedback summary for {current_date}:")
    print(chat_completion.choices[0].message.content)
    print(f"\nEnd of feedback for {current_date}\n###########################\n")

    # Move to the next day
    current_date += timedelta(days=1)
