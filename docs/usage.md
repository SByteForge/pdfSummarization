# Usage Instructions

## Prerequisites

Summarization runs against a local LLM via [Ollama](https://ollama.com). Before starting the app, make sure Ollama is installed, running, and has a model pulled:

```bash
ollama pull llama3.2:1b
```

The app defaults to `OLLAMA_URL=http://localhost:11434` and `OLLAMA_MODEL=llama3.2:1b` — override either via environment variables or a `.env` file if you're using a different model or a remote Ollama instance.

## How to Use the PDF Summarizer

1. **Start the Application**:
   - Run the following command in your terminal:
     ```bash
     streamlit run src/streamlit_app.py
     ```
   - Or, using Docker:
     ```bash
     docker build -t pdf-summarizer:local .
     docker run -p 8501:8501 \
       -e OLLAMA_URL=http://host.docker.internal:11434 \
       -e OLLAMA_MODEL=llama3.2:1b \
       pdf-summarizer:local
     ```

2. **Upload a PDF Document**:
   - Use the file uploader interface to select and upload your PDF document.

3. **Generate Summary**:
   - Click on the "Generate Summary" button to process the document.
   - Wait a few seconds for the summary to be generated.

4. **View the Summary**:
   - The generated summary will appear below the upload section.

### Tips

- Ensure your PDF files are well-formatted for better text extraction.
- Experiment with different documents to see how the summarization varies.
