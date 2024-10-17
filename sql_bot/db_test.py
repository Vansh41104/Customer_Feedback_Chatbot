import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

print(sqlalchemy.__version__)

engine = create_engine("postgresql+psycopg2://admin:password@localhost/kanari_insights", echo=True)

print(engine)

engine.connect()

insp = sqlalchemy.inspect(engine)
db_list = insp.get_schema_names()
print(db_list)

with engine.connect() as connection:
    result = connection.execute(text("select comment from public.chatbot_data limit 10"))
    for row in result:
        print("comment:", row.comment)
