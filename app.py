__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import os
import time
import tempfile
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader
import docx2txt

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = st.secrets["API_KEY"]
genai.configure(api_key = st.secrets["API_KEY"])

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key = api_key)

def upload_to_gemini(file):
    """Uploads the given file to Gemini."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        uploaded_file = genai.upload_file(tmp_file_path, mime_type=file.type)
        return uploaded_file
    finally:
        os.remove(tmp_file_path)  # Clean up the temporary file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(2)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

def process_documents(uploaded_files):
    documents = []
    for file in uploaded_files:
        if file.type == "text/plain":
            # For text files
            file_contents = file.getvalue().decode("utf-8", errors="ignore")
            documents.append(file_contents)
        elif file.type == "application/pdf":
            # For PDF files
            pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
            file_contents = ""
            for page in pdf_reader.pages:
                file_contents += page.extract_text()
            documents.append(file_contents)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # For DOCX files
            file_contents = docx2txt.process(io.BytesIO(file.getvalue()))
            documents.append(file_contents)
        else:
            st.warning(f"Unsupported file type: {file.type}. Skipping this file.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_text("\n".join(documents))
    
    vectorstore = Chroma.from_texts(split_docs, embeddings)
    return vectorstore

# Streamlit UI
st.title("RaDoG - Your Personalized AI Chatbot")

# File uploader
uploaded_files = st.file_uploader("Upload one or more documents", accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Uploading and processing files..."):
        gemini_files = [upload_to_gemini(file) for file in uploaded_files]
        wait_for_files_active(gemini_files)
        vectorstore = process_documents(uploaded_files)
    
    st.success("Files uploaded and processed. Let's start chatting!")

    # Create the model
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Initialize chat session
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your documents"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            context = vectorstore.similarity_search(prompt, k=3)
            context_text = "\n".join([doc.page_content for doc in context])
            
            response = st.session_state.chat_session.send_message(
                f"Context: {context_text}\n\nQuestion: {prompt}\n\nPlease answer the question based on the given context."
            )
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

else:
    st.info("Please upload one or more documents to begin.")
