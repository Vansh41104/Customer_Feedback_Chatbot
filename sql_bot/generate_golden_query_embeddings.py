from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import shutil
from golden_queries import golden_queries

load_dotenv()

vector_store_directory = os.environ.get('VECTOR_STORE_DIRECTORY')

print('Cleaning up the persist directory')
for filename in os.listdir(vector_store_directory):
    file_path = os.path.join(vector_store_directory, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
print('Done')

load_dotenv()

print('Generating embeddings')
documents = []
for golden_query in golden_queries:
    for question in golden_query.get_questions():
        for query in golden_query.get_sql_queries():
            documents.append(Document(
                page_content=f"Question: {question}\nSQL Query: {query}"
            ))

embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(documents, embedding=embeddings, persist_directory=vector_store_directory)
db.persist()

print('Done')
