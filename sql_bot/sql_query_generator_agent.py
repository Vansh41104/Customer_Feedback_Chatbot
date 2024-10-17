import os

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.utilities.sql_database import SQLDatabase
from datetime import date

from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
from langchain_openai import OpenAI

from sql_toolkit import SQLDatabaseToolkit

load_dotenv()


class SqlQueryAgent():
    def __init__(self, llm_model: str, data_source_uri: str, verbose: bool = True):
        self.llm_model = llm_model
        self.agent = self.create_database_agent(self.llm_model, data_source_uri, verbose)
        self.verbose = verbose

    def run(self, user_question, question_answer_pairs):

        query = f"""
You are a PostgreSQL query generator expert. 

Based on the question, return the full sql query needed to fulfill the query

You should query the "chatbot_data" table for the data

Here are some example query and SQL statement pairs to help guide you. Use these as guides only.

{question_answer_pairs}        

Return the query only, do not pad it with unnecessary text
{user_question}

The current date is {date.today()}

Do not apply any ORDER BY or LIMIT clauses to the query

IMPORTANT: Do not use the nps column inside a WHERE clause EVER

Enclose the SQL query in a code block like so:
```sql
{{SQL Query}}
```

SQL Query:
"""
        if self.verbose:
            print(query)

        result = self.agent.invoke(query)

        if self.verbose:
            print('The Pre Sanitized Result is:', result)

        return self.sanitize_sql_query(result['output'])

    def sanitize_sql_query(self, query: str):
        splitted = query.split("```")
        splitted = splitted[1]

        splitted = splitted.strip()

        if splitted.startswith('sql'):
            splitted = splitted[3:]

        splitted = splitted.strip()

        # print('The splitted is:', splitted)

        # query = query.lstrip('SQL Query:')
        # query = query.strip('\n')
        # query = query.strip('')
        # query = query.strip('\n')
        # if query.startswith('```sql'):
        #     query = query.strip('```')
        #     query = query.lstrip('sql')
        #
        return splitted

    def create_database_agent(self, llm_model: str, data_source_uri: str, verbose: bool = True):
        return self._create_database_agent(
            db_uri=data_source_uri,
            prompt=sql_query_generator_prompt,
            model=llm_model,
            temperature=0,
            verbose=verbose,
        )

    def _create_database_agent(
            self,
            db_uri,
            temperature,
            model,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            prompt=None,
    ):
        customer_feedback_db = SQLDatabase.from_uri(db_uri)
        toolkit = SQLDatabaseToolkit(db=customer_feedback_db, llm=OpenAI(temperature=temperature, verbose=verbose))

        # llm = ChatOpenAI(temperature=temperature, model=model, verbose=verbose)

        llm = AzureChatOpenAI(
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        )

        return create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=verbose,
            agent_type=agent_type,
            prefix=prompt,
        )


sql_query_generator_prompt = f"""
You are a data analyst working for an automotive company that provides servicing for customers vehicles at
a number of different locations. You have been tasked with analysing customer feedback data to help staff

Your task is to return valid SQL queries based on the question asked by the staff, and based on the information
available in the database

Based on the question, return the full sql query needed to fulfill the query       

If asked for the "Best" or "Worst" feedback, do not limit the query to only 1 result. Return all the feedback

Do not apply any ORDER BY or LIMIT clauses to the query 

Do not use the nps column inside a WHERE clause EVER
"""
