from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

vector_store_directory = os.environ.get('VECTOR_STORE_DIRECTORY')

def get_question_answer_examples(query):
    persist_directory = vector_store_directory
    db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
    retriever = db.as_retriever(
        search_kwargs={"k": 2, "score_threshold": 0.5},
        search_type="similarity_score_threshold",
    )

    docs = retriever.invoke(query)

    response = ''
    for doc in docs:
        response += doc.page_content + "\n\n"

    return response
