from typing import Any, Dict, List
from langchain import PromptTemplate, LLMChain
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os

load_dotenv()

import pinecone

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
)


def run_llm(query: str, chat_history: List[Dict[str, Any]], node: str) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = Pinecone.from_existing_index(
        index_name="db1", embedding=embeddings, namespace=node
    )

    model = ChatOpenAI(verbose=True, temperature=0, model="gpt-3.5-turbo-16k")

    prompt_template = """You answer in a long and detailed manner with as many code samples as possible and long elaborate explanations.
    Use the following pieces of context to answer the question at the end.

    {context}

    Question: {question}

    Let's think step by step.

    Helpful Answer:"""
    QA_PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. At the end of standalone question add this 'Answer is as much details as possible' If you do not know the answer reply with 'I am sorry'.
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=docsearch.as_retriever(search_type="similarity", search_kwargs={"k":5}),
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
        verbose=True,
    )

    # test this parameter
    # vectordbkwargs = {"search_distance": 1}
    # return qa({"question": query})

    # dont use chat history
    return qa({"question": query, "chat_history": ""})



if __name__ == "__main__":
    print(run_llm("What is a retrievalQA chain ?"))


    #search_type="similarity", search_kwargs={"k":1}
    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=model,
    #     retriever=docsearch.as_retriever(search_type="similarity", search_kwargs={"k":5}),
    #     condense_question_llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k'),
    #     condense_question_prompt=CUSTOM_QUESTION_PROMPT,
    #     combine_docs_chain_kwargs={"prompt": QA_PROMPT},
    #     return_source_documents=True,
    #     verbose=True,
    # )