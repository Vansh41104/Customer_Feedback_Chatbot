from typing import Union
import re


class GoldenQuery:
    def __init__(self, questions: Union[str, list[str]], sql_queries: Union[str, list[str]]):
        self.questions = [questions] if isinstance(questions, str) else questions
        self.sql_queries = [sql_queries] if isinstance(sql_queries, str) else sql_queries

    def get_questions(self):
        return self.questions

    def get_sql_queries(self):
        return self.sql_queries

    def is_valid_query(self, sql_query: str):
        # replace new lines with a space
        sql_query = self.format_query(sql_query)

        for golden_query in self.sql_queries:
            if sql_query == golden_query.lower().strip():
                return True

        return False

    @staticmethod
    def format_query(query: str):
        # replace new lines with a space
        query = re.sub(r'\n', ' ', query)
        # make sure there is only one space between words
        query = re.sub(r'\s+', ' ', query)
        # remove the last space
        query = query.strip()
        # make all letters small caps
        return query.lower()
