from langchain_community.utilities.sql_database import SQLDatabase

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool


def create_sql_query_runner_tool(data_source_uri: str):
    db = SQLDatabase.from_uri(data_source_uri)

    return QuerySQLDataBaseTool(
        db=db,
        description=run_database_query_tool_description
    )


run_database_query_tool_description = (
    "Input to this tool is a detailed and correct SQL query, output is a "
    "result from the database. If the query is not correct, an error message "
    "will be returned. If an error is returned, rewrite the query, check the "
    "query, and try again. If you encounter an issue with Unknown column "
    f"'xxxx' in 'field list', use XXXX "
    "to query the correct table fields."
)
