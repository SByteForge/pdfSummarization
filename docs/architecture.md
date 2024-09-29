# Architecture Overview

The PDF Summarizer is built using a modular architecture that separates concerns for better maintainability and scalability. Below is a high-level overview of the architecture components:

## Components

- **User Interface**: Built with Streamlit, allowing users to interact with the application easily.
- **PDF Reader**: Extracts text from uploaded PDF files using the `pypdf` library.
- **Text Processing**: Utilizes LangChain for text chunking and embedding generation.
- **Summarization Engine**: Integrates with OpenAI's API to generate summaries based on the processed text.
- **Configuration Management**: Uses a `config.py` file to manage environment variables and application settings.

## Data Flow

1. User uploads a PDF file.
2. The PDF Reader extracts text from the file.
3. The extracted text is processed into manageable chunks.
4. The chunks are embedded and stored in a knowledge base.
5. A summarization request is made to the OpenAI API using the processed chunks.
6. The summary is displayed back to the user in the Streamlit interface.
