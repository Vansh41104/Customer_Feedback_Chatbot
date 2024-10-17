import os

import chainlit as cl

from dotenv import load_dotenv
from sql_query_generator_agent import SqlQueryAgent
from sql_query_runner_tool import create_sql_query_runner_tool
from query_result_summariser import summarise_query
from langchain.chains import ConversationChain
from langsmith import traceable
from qa_few_shot_prompt_selector import get_question_answer_examples
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm_model = 'gpt-3.5-turbo-0125'

# data_source_uri = 'sqlite:///auto_service.db'
data_source_uri = os.environ.get('DATA_SOURCE_URI')

sql_query_generator_agent = SqlQueryAgent(llm_model, data_source_uri)
execute_database_query_tool = create_sql_query_runner_tool(data_source_uri)

llm = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)

# print(model.invoke("Tell me a joke"))
#
# sys.exit()
#
# llm = ChatOpenAI(
#     temperature=0,
#     model_name=llm_model,
# )

conversation = ConversationChain(llm=llm)

questions = []

bot_opening_message = """Hello there, I'm your senior data analyst assistant, and I'm here to help you analyse the
customer feedback from your various Service Centres. You can ask thing like:
- List the top things we are doing well in March 2023?
- How many responses do we have in January 2023 by brand?
- What is the worst feedback from my INFINITI Service Mussafah branch?
 
To clear the chat history you can type "clear" or "restart".

You can also enable or disable chat history by typing "enable history" or "disable history". It is disabled by default.
 
Let's get started. How can I help you?
"""


def validate_query_filters_by_campaign(query: str, campaign: str):
    query_lower_case = query.lower()
    campaign_lower_case = campaign.lower()

    is_valid = False

    if query_lower_case.find(f"where survey_source = '{campaign_lower_case}'") > 0 or query_lower_case.find(
            f"and survey_source = '{campaign_lower_case}'") > 0:
        is_valid = True

    return is_valid


def validate_query_filters_by_customer(query: str, customer_id: int):
    query_lower_case = query.lower()

    is_valid = False

    if query_lower_case.find(f"where customer_id = {str(customer_id)}") > 0 or query_lower_case.find(
            f"and customer_id = {str(customer_id)}") > 0:
        is_valid = True

    return is_valid


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("questions", [])
    cl.user_session.set("enable_chat_history", False)

    await cl.Message(content=bot_opening_message).send()


@traceable
@cl.on_message
async def main(message: str):
    global questions

    # campaign_filter = 'Body Shop'
    campaign_filter = None
    customer_id_filter = 62

    user_question = message.content

    if user_question == 'clear' or user_question == 'restart':
        questions = cl.user_session.set("questions", [])
        await cl.Message(content='Chat history cleared').send()
        return

    if user_question == 'disable history':
        cl.user_session.set("enable_chat_history", False)
        await cl.Message(content='Chat history disabled').send()
        return

    if user_question == 'enable history':
        cl.user_session.set("enable_chat_history", True)
        await cl.Message(content='Chat history enabled').send()
        return

    questions = cl.user_session.get("questions")

    questions = questions + [user_question]
    cl.user_session.set("questions", questions)

    enable_chat_history = cl.user_session.get("enable_chat_history")

    user_question_with_filters = user_question

    if campaign_filter is not None:
        user_question_with_filters = user_question_with_filters + ". Get only results where the survey_source = 'Body Shop'"

    if customer_id_filter is not None:
        user_question_with_filters = user_question_with_filters + ". IMPORTANT: Get only results where the customer_id = " + str(customer_id_filter)

    if len(questions) > 1 and enable_chat_history:
        if len(questions) > 7:
            del questions[:4]

        final_questions_list = '\n\n'.join(questions)

        my_prompt = f"""
        From the following list of questions, please generate a coherent question
        that tells us what the final question in this list is asking for:

        {final_questions_list}

        Final question:
        """

        print('User questions:')
        print(final_questions_list)

        response = llm.invoke(my_prompt)
        print('Combine query')
        print(response)
        user_question = response.content
        # await cl.Message(content='The final question will be:\n' + user_question).send()

    question_answer_pairs = get_question_answer_examples(user_question)

    await cl.Message(content='The matching golden queries are :\n' + question_answer_pairs).send()

    sql_query = sql_query_generator_agent.run(user_question_with_filters, question_answer_pairs)

    if campaign_filter is not None:
        retry = 0
        while validate_query_filters_by_campaign(sql_query, campaign_filter) is False and retry < 3:
            retry += 1
            print('Retrying to generate query with campaign filter. Retry: ' + str(retry))
            sql_query = sql_query_generator_agent.run(user_question_with_filters, question_answer_pairs)

        if validate_query_filters_by_campaign(sql_query, campaign_filter) is False:
            await cl.Message(content='Unable to correctly filter query by campaign\n').send()
            return

    if customer_id_filter is not None:
        retry = 0
        while validate_query_filters_by_customer(sql_query, customer_id_filter) is False and retry < 3:
            retry += 1
            print('Retrying to generate query with campaign filter. Retry: ' + str(retry))
            sql_query = sql_query_generator_agent.run(user_question_with_filters, question_answer_pairs)
            print('-----------------------------------')
            print('SQL Query: ' + sql_query)
            print('-----------------------------------')

        if validate_query_filters_by_customer(sql_query, customer_id_filter) is False:
            await cl.Message(content='Unable to correctly filter query by campaign\n').send()
            return

    print('\nThe SQL query used to retrieve the data will be:')
    print(sql_query)

    await cl.Message(content='The SQL query used to retrieve the data will be:\n' + sql_query).send()

    # query_description = llm.invoke(f"""
    # Give me a description of the following SQL query in plain English. Do not mention that it is an SQL query.
    # Just return a description of what the query is truing to find
    #
    # SQl Query: {sql_query}
    #
    # Description:
    # """)
    #
    # await cl.Message(content='The SQL query used to retrieve the data will be:\n' + query_description.content).send()

    print('\nNow executing the query against the database:')
    sql_query_result = execute_database_query_tool.run(sql_query)
    print('\nThe SQL query results are :')
    print(sql_query_result)

    result = sql_query_result.lstrip('[(\'').rstrip(',\')]')
    result = result.replace('",), ', '\',), ')
    result = result.replace(', ("', ', (\'')
    result = result.split('\',), (\'')

    print('\nAs dict:')
    print(result)

    final_result = "\n".join(str(line) for line in result)

    if len(sql_query_result) == 0:
        await cl.Message(content='We could not retrieve any relevant information regarding your question').send()
        return

    print('\nSummarising the query results based on the users question')
    summary = await summarise_query(final_result, user_question, llm, sql_query)

    print('\nThe response based on the users question is:')
    print(summary)

    questions = questions + [summary]

    # Send a response back to the user
    await cl.Message(content=summary).send()
