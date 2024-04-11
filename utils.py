# Defining two functions for converting a PDF file to text and generating embeddings for the text.
# The pdf2text function takes a PDF file as input and returns the text and chunks of the text.
# The embeddings_from_chunks function takes chunks of text as input and returns embeddings for the chunks.

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

def pdf2text(file):

    pdf_reader = PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = CharacterTextSplitter(
        separator="\n",  
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return text, chunks

def embeddings_from_chunks(chunks):

    model = HuggingFaceEmbeddings()
    
    return FAISS.from_texts(chunks, model)
