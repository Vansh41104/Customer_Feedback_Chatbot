import sqlite3

import pandas as pd

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_sqlite_db_from_csv(csv_url, db_name, table_name="employee_data"):
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Load CSV file into a Pandas dataframe directly from the URL
    data_df = pd.read_csv(csv_url)

    # Write the dataframe to the SQLite database
    data_df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()
    print(f"Database {db_name} with table {table_name} created successfully!")

create_sqlite_db_from_csv("ama-2023-2024-feedback.csv", db_name="auto_service.db", table_name="feedback")
# create_sqlite_db_from_csv("../data/pre_processed/preprocessed_auto_service.csv", db_name="auto_service.db", table_name="feedback_topic_sentiment")


