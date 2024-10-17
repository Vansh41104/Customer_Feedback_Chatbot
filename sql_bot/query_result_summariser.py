from langchain.text_splitter import CharacterTextSplitter

from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
import re

prompts_samples = """
    Try to keep the information in bullet point format, and about 200 words in length. Respond in a friendly and
    informative manner
    
    Do not feel obliged to provide a long response, just the key insights. Do provide responses that are not related to
    information from the target data
"""


async def summarise_query(sql_query_result, user_question, llm, sql_query):

    # strip whitespace and multiple blank lines
    sql_query_result = re.sub(r'(\n\s*)+\n', '\n\n', sql_query_result)

    print('Word count of query result: ', len(sql_query_result.split()))

    print('Query result: ', sql_query_result)

    print('Result length: ', len(sql_query_result))
    # sys.exit()

    prompt_template = f"""
You are an assistant working for an automotive company that provides servicing for customers vehicles at
a number of different locations. You have been tasked with analysing customer feedback data to help staff
understand what customers are saying about the service they provide.
 
You will be provided with information in CSV format
from our datawarehouse. Your task is to pull out insights from the data based on the questions asked by the staff.

Keep the responses no longer than 150 words long. Have longer response
if there is a lot of context to summarise. Otherwise keep the response short and sweet. Only talk about the content
in the response. Do not include suggestions for the need to collect for data e.t.c. And only answer the question
asked by the user. If they want specific information, provide only that. Do not provide additional information, 
or suggestions for improvement, unless specifically asked for. Lean towards providing the answers in bullet point
   
The results below describe the following question:

Question: {user_question}

Results:

### START OF RESULTS

{{docs}}

### END OF RESULTS

And the question asked by the staff is: "{user_question}"

Use all the information from the results in providing the final answer

Answer:"""

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=35000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=12000, chunk_overlap=0
    # )

    split_docs = text_splitter.create_documents([sql_query_result])

    print('Split docs: ', len(split_docs))

    # Map
    if len(split_docs) > 10:
        return """There is too much information to summarise related to your query. Try asking the same question but time
bounding it. For example ask for all feedback "in March 2024", or all feedback from "last month"""

    if len(split_docs) > 1:
        map_template = """The following is a set of documents
        {docs}
        Based on this list of docs, please identify the main themes 
        Helpful Answer:"""
        map_prompt = PromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        # Run chain
        reduce_template = """The following is set of summaries:
        {docs}
        Take these and distill it into a final, consolidated summary of the main themes. 
        Helpful Answer:"""
        reduce_prompt = PromptTemplate.from_template(reduce_template)
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=16000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        response = map_reduce_chain.invoke(split_docs)

        return response['output_text']

    else:
        print('Not Summarising')
        prompt_template = PromptTemplate.from_template(prompt_template)

        prompt = prompt_template.format(docs=sql_query_result)

        print('\nprompt')
        print(prompt)

        response = llm.invoke(prompt)

        print(response)

        return response.content

def get_text_chunks_langchain(text):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs
