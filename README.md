## DocSumQA: A Streamlit App for AI-Powered Document Summarization and Question Answering

# Description

DocSumQA is a user-friendly Streamlit application that empowers you to extract key insights and ask questions about PDF documents. It leverages the power of large language models (LLMs) to provide:

- Automatic Summarization: Generate concise summaries of uploaded PDFs, capturing the essence of the document.
- Context-Aware Question Answering: Ask in-depth questions related to the document's content, and receive informative, contextually aware answers from the LLM.


# Prerequisites:
- Ensure you have Python 3.x and pip installed.
- Clone the Repository: Use git clone https://github.com/your-username/DocSumQA.git to clone this repository.
- Create a Virtual Environment (Recommended): Create a virtual environment to isolate project dependencies. You can use tools like venv or conda.
- Install Dependencies: Navigate to the project directory and run pip install -r requirements.txt to install the required libraries.

# Usage

- Execute streamlit run app.py (or the equivalent command depending on your setup) to launch the DocSumQA app in your web browser (usually at http://localhost:8501).
- Upload a PDF: Click the "Upload the document" button and select the PDF file you want to analyze.

# Summarization

After uploading the PDF, DocSumQA will automatically generate a summary of the document's content.
Question Answering

- In the text input field, type your question about the document.
- Ensure your question is related to the document's content.
- Click "Enter" to submit your question.
- DocSumQA will process your question using the LLM and the document context to provide an informative answer.
- You can ask multiple questions to delve deeper into the document.

# Customization (Optional)

- This repository provides the groundwork for customization. You can experiment with different LLM models (see the model_id variables in app.py and model.py) to explore their capabilities.
- Refer to the documentation of the Langchain and Hugging Face libraries for further customization options.

# Contributing

We welcome contributions to this project! Feel free to create a pull request on GitHub if you have improvements or suggestions. Make sure to follow our contribution guidelines (if any).
