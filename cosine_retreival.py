# This code is a Streamlit app that allows users to upload a PDF document and ask questions about it.
# The app uses a language model to generate answers to the user's questions based on the content of the document.
# The app uses the Hugging Face Hub to load the language model and the Langchain library to process the document and generate answers.


from dotenv import load_dotenv
import streamlit as st
from utils import *
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub
import os 


load_dotenv()
st.set_page_config(page_title="DocSumQA")
st.header("Ask any question related to the document!")

pdf = st.file_uploader("Upload the document", type="pdf")

if pdf is not None:

    _, chunks = pdf2text(pdf)
    context = embeddings_from_chunks(chunks)

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "{enter api key}" 
    llm = HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct", model_kwargs={"temperature": 0.1, "max_length": 512})
   

    while True:
        
        user_question = st.text_input("Ask a question (enter exit to break): ")
        
        if user_question != 'exit':

            docs = context.similarity_search(user_question)
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=user_question)

            st.write(response)

        elif user_question.lower() == 'exit':
            break

        else:
            print("invalid response")
