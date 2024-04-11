# Streamlit app that allows users to upload a PDF document and ask questions about it.
# The app uses a language model to generate answers to the user's questions based on the content of the document.
# The app uses the Hugging Face Hub to load the language model and the Langchain library to process the document and generate answers.
# The app also uses a history-aware retriever to take into account the chat history when generating answers.


from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.llms import HuggingFacePipeline
from dotenv import load_dotenv
import streamlit as st
from utils import *
from model import create_query

load_dotenv()
st.set_page_config(page_title="DocSumQA")
st.header("Ask any question related to the document!")

pdf = st.file_uploader("Upload the document", type="pdf")

if pdf is not None:

    _, chunks = pdf2text(pdf)
    context = embeddings_from_chunks(chunks)
    retriever = context.as_retriever()
    
    query_pipeline = create_query('enter the model ID you wish to use here')
    llm = HuggingFacePipeline(pipeline=query_pipeline)
    
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    chat_history = []
    
    while True:
        question = st.text_input("Ask a question (enter exit to break): ")

        if question != 'exit':
            ai_msg = rag_chain.invoke({"input": question, "chat_history": chat_history})
            print(ai_msg["answer"])

        elif question == 'exit':
            break
        
        else:
            print('invalid argument')
