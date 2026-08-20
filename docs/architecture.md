# Architecture Overview

The PDF Summarizer is built using a modular architecture that separates concerns for better maintainability and scalability. Below is a high-level overview of the architecture components:

## Components

- **User Interface**: Built with Streamlit, allowing users to interact with the application easily.
- **PDF Reader**: Extracts text from uploaded PDF files using the `pypdf` library.
- **Text Processing**: Utilizes LangChain to chunk text and generate local embeddings via `sentence-transformers`, indexed with FAISS for retrieval.
- **Summarization Engine**: Generates summaries using a locally-hosted LLM served through Ollama (`langchain-ollama`) — no external API calls.
- **Configuration Management**: Uses a `config.py` file to manage environment variables (`OLLAMA_URL`, `OLLAMA_MODEL`) and application settings.

## Data Flow

1. User uploads a PDF file.
2. The PDF Reader extracts text from the file.
3. The extracted text is processed into manageable chunks.
4. The chunks are embedded locally and stored in a FAISS knowledge base.
5. A summarization request is made to the local Ollama-served LLM using the retrieved chunks.
6. The summary is displayed back to the user in the Streamlit interface.

## Deployment

The application is packaged as a multi-stage, non-root Docker image. Per-environment configuration (`dev`/`qa`/`prod`) lives in `deploy/environments/`, consumed by a deployment chart maintained in a separate platform repository — this repo owns the application and its values only, not the chart or cluster wiring.
