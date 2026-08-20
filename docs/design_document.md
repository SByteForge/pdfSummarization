# PDF Summarizer Design Document

#### 1. **Project Overview**
The **PDF Summarizer** is an application that reads PDF documents and generates concise summaries using a locally-hosted Large Language Model (LLM). The application is built using **LangChain** for the retrieval/summarization pipeline and **Streamlit** for creating a user-friendly web interface. It allows users to upload PDF files, which are processed for text extraction, embedded and retrieved locally, and then summarized using an LLM served through Ollama — no external API calls.

#### 2. **Key Features**
- **PDF Reading**: Extracts text from PDF files for further processing.
- **Local Retrieval**: Chunks text, embeds it locally with `sentence-transformers`, and retrieves relevant chunks via FAISS.
- **Summarization**: Leverages a self-hosted LLM via Ollama to generate summaries of extracted text — free of paid API dependency.
- **Interactive UI**: A web-based interface built using Streamlit, allowing users to upload PDFs and view summaries in real-time.

#### 3. **Architecture Design**
The application follows a modular structure, ensuring that the components for PDF extraction, summarization, and the UI are decoupled for scalability and maintainability. The main architectural components include:

- **Frontend (Streamlit)**: Provides the user interface, allowing users to upload PDFs and view summaries.
- **Backend (LangChain & LLM)**: Handles the PDF text extraction and LLM-based summarization.
- **Storage**: Stores uploaded PDFs and their summaries temporarily for processing.

##### **Component Diagram**
```
|-------------------------------|
|           Frontend             |
|     (Streamlit Web App)        |
|-------------------------------|
            | Upload PDF
            v
|-------------------------------|
|           Backend              |
|  - PDF Reader (pypdf)          |
|  - Retrieval (FAISS + local    |
|    sentence-transformers)      |
|  - LLM Integration (Ollama)    |
|-------------------------------|
            |
            v
|-------------------------------|
|          Storage               |
|  - Temporary PDF storage       |
|  - Text summaries              |
|-------------------------------|
```

#### 4. **Technologies Used**
- **Python 3.12+**: Core language for the project.
- **LangChain**: Framework for building applications with LLMs.
- **Streamlit**: Library for building interactive web applications.
- **pypdf**: Tool for extracting text from PDF documents.
- **sentence-transformers + FAISS**: Local embedding generation and similarity search.
- **Ollama** (via `langchain-ollama`): Self-hosted LLM integration for summarization tasks — no paid API dependency.

#### 5. **Detailed Component Design**
1. **PDF Reader**:
   - Uses `pypdf` to extract text from uploaded PDFs.
   - Handles multi-page PDF documents.
   - Processes the raw text for input into the summarization model.

2. **Summarization Component**:
   - Integrates with LangChain for managing the pipeline of text processing.
   - The core summarization logic communicates with a local Ollama server, sending retrieved chunks and receiving summarized output.
   - Supports configurable model selection via `OLLAMA_MODEL`.

3. **Interactive UI**:
   - Built using Streamlit for easy-to-use, real-time interaction.
   - Allows users to upload PDFs and displays summaries in a clean, simple interface.
   - Handles file uploads and calls backend components to process the PDF and return summaries.

#### 6. **Project Structure**
- **data/**: Stores raw and processed PDF files.
- **docs/**: Documentation for the project.
- **src/**: Source code for the PDF reader, text processing, summarization logic, and Streamlit app.
  - **pdf_reader.py**: Handles PDF text extraction.
  - **text_processor.py**: Chunks text and builds a local FAISS knowledge base.
  - **openai_client.py**: Interacts with LangChain and Ollama for summarization.
  - **summarizer.py**: Orchestrates the read → embed → summarize pipeline.
  - **streamlit_app.py**: Hosts the Streamlit web app.
  - **exceptions.py**: Application-specific error types.
- **test/**: Contains unit tests.
- **deploy/environments/**: Per-environment (`dev`/`qa`/`prod`) configuration values.
- **Dockerfile**: Multi-stage, non-root container image.
- **.github/workflows/**: CI pipeline (lint + test).
- **.env**: Optional, for overriding `OLLAMA_URL`/`OLLAMA_MODEL`.

#### 7. **Installation & Setup**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SByteForge/pdfSummarization.git
   cd pdfSummarization
   ```
2. **Set up the Virtual Environment**:
   - Create a virtual environment (optional):
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - For macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - For Windows:
       ```bash
       venv\Scripts\activate
       ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Ollama and pull a model**:
   ```bash
   ollama pull llama3.2:1b
   ```
5. **Set Up Environment Variables (optional)**:
   - Create a `.env` file to override the defaults:
     ```
     OLLAMA_URL=http://localhost:11434
     OLLAMA_MODEL=llama3.2:1b
     ```

#### 8. **Usage**
To start the application:
1. Run the Streamlit app:
   ```bash
   streamlit run src/streamlit_app.py
   ```
2. Open the browser, upload your PDF files, and view the generated summaries.

#### 9. **Testing**
- The project includes unit tests for individual components and integration tests for end-to-end functionality.
- To run the tests:
  ```bash
  pytest
  ```

#### 10. **Future Enhancements**
- **Additional File Formats**: Support for DOCX, TXT, and other file formats.
- **Customization**: Allow users to customize summarization parameters (e.g., summary length, detail level).
- **Export Options**: Enable users to download the summary as a text file or PDF.
- **Caching**: Cache processed summaries to avoid repeated LLM calls for the same document.

#### 11. **Contributions**
- Contributions are welcome! Feel free to submit issues or pull requests.

