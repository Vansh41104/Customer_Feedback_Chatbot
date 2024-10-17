import os

import chainlit as cl
import re
from dotenv import load_dotenv
from sql_query_generator_agent import SqlQueryAgent
from qa_few_shot_prompt_selector import get_question_answer_examples
from golden_queries import golden_queries
from golden_query import GoldenQuery

load_dotenv()

data_source_uri = os.environ.get('DATA_SOURCE_URI')

llm_model = 'gpt-3.5-turbo-0125'

sql_query_generator_agent = SqlQueryAgent(llm_model, data_source_uri, verbose=False)

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"
red = "\033[0;31m"

passes = 0
fails = 0
total = 0
tests = []

limit = 70

for golden_query in golden_queries:
    for user_question in golden_query.get_questions():

        if limit is not None and total >= limit:
            break

        total += 1

        golden_sql = golden_query.get_sql_queries()[0].lower().strip()
        qa_samples = get_question_answer_examples(user_question)
        print(f"{white}Processing {total} of {len(golden_queries)}\n")

        print(f"{green}\nUser Question: {user_question}\n{white}")
        print(f"{yellow}\nGolden SQL: {golden_sql}\n{white}")
        print(qa_samples)

        sql_query = sql_query_generator_agent.run(user_question, cl)
        print(f"{yellow}SQL Query: {GoldenQuery.format_query(sql_query)}\n{white}")

        is_pass = golden_query.is_valid_query(sql_query)

        if is_pass:
            passes += 1
            print(f"{green}PASS\n{white}")
        else:
            print(f"{red}FAIL\n{white}")
            fails += 1

        test = {
            "user_question": user_question,
            "golden_sql": golden_sql,
            "sql_query": GoldenQuery.format_query(sql_query),
            "status": "PASS" if is_pass else "FAIL"
        }

        tests.append(test)

        print('-----------------------------------\n')

print(f"{green}Passes: {passes}\nFails: {fails}\nTotal: {total}\n{white}")

print('-----------------------------------\n')

for test in tests:
    print(f"{green}User Question{white}: {test['user_question']}")
    print(f"{green}Golden SQL{white}: {test['golden_sql']}")
    print(f"{green}SQL Query{white}: {test['sql_query']}")
    print(f"{green}Status{white}: {green if test['status'] == 'PASS' else red}{test['status']}{white}")
    print('-----------------------------------\n\n')

print('Failed Tests Summary')

for test in tests:
    if test['status'] != 'PASS':
        print(f"{green}User Question{white}: {test['user_question']}")
        print(f"{green}Golden SQL{white}: {test['golden_sql']}")
        print(f"{green}SQL Query{white}: {test['sql_query']}")
        print(f"{green}Status{white}: {green if test['status'] == 'PASS' else red}{test['status']}{white}")
        print('-----------------------------------\n\n')


print(f"{green}Passes: {passes}\nFails: {fails}\nTotal: {total}\n{white}")
