# Gemini-powered Document Q&A

This Streamlit application leverages Google's Gemini AI to provide a powerful document question-answering system. Users can upload multiple documents and engage in a conversational interface to ask questions about the content of these documents.

## Features

- Multi-document upload support (TXT, PDF, DOCX)
- Document processing and indexing using LangChain and Chroma
- Conversational interface powered by Google's Gemini AI
- Retrieval-Augmented Generation (RAG) for accurate answers

## Installation

1. Clone this repository
2. Create a virtual environment and activate it
3. Install the required packages
4. Create a `.env` file in the root directory and add your Gemini API key (replace the st.secrets with dotenv code snippet)
## Usage

1. Run the Streamlit app

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload one or more documents using the file uploader.

4. Wait for the documents to be processed and indexed.

5. Start asking questions about the uploaded documents in the chat interface.

## How it Works

1. Document Upload: The app accepts multiple document uploads (TXT, PDF, DOCX).
2. Processing: Uploaded documents are processed and text is extracted.
3. Indexing: The extracted text is split into chunks and indexed using Chroma vector store.
4. Question-Answering: When a user asks a question, the app retrieves relevant context from the indexed documents.
5. Gemini AI: The question and retrieved context are sent to Gemini AI for generating an accurate answer.
6. Response: The AI-generated answer is displayed to the user in a conversational interface.

## Dependencies

- streamlit
- google-generativeai
- python-dotenv
- langchain
- chromadb
- PyPDF2
- docx2txt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
