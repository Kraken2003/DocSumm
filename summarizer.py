from docsumutils import docsumm
from utils import pdf2text
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
st.set_page_config(page_title="DocSum")
st.header("Creating Summaries for you!")

pdf = st.file_uploader("Upload the document", type="pdf")

text,_ = pdf2text(pdf)

llm = docsumm('enter the model ID you wish to use here')

print(llm.run(text))
