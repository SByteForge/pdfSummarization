# PDF Summarizer

## Overview

The **PDF Summarizer** project is an application designed to read PDF files and generate concise summaries using a locally-hosted Large Language Model (LLM). Text is chunked and embedded locally, retrieved via FAISS, and summarized by an LLM served through [Ollama](https://ollama.com) — no external API keys or paid services required. The project uses LangChain for the retrieval/summarization pipeline and Streamlit for the interactive user interface.

## Features

- **PDF Reading**: Extracts text from PDF documents.
- **Local Retrieval**: Chunks and embeds text locally (`sentence-transformers`) and indexes it with FAISS.
- **Local Summarization**: Uses a self-hosted LLM via Ollama to generate summaries — no data leaves your machine.
- **Interactive UI**: Provides a web-based interface with Streamlit for easy interaction.
- **Containerized**: Ships with a multi-stage, non-root Dockerfile.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Pip (Python package installer)
- [Ollama](https://ollama.com) installed and running, with a model pulled (default: `llama3.2:1b`)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SByteForge/pdfSummarization.git
    cd pdfSummarization
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Pull an Ollama model** (if you don't already have one):

    ```bash
    ollama pull llama3.2:1b
    ```

5. **Configure environment variables (optional):**

    The app talks to Ollama over `OLLAMA_URL` (default `http://localhost:11434`) and uses `OLLAMA_MODEL` (default `llama3.2:1b`). Override either in a `.env` file if needed:

    ```plaintext
    OLLAMA_URL=http://localhost:11434
    OLLAMA_MODEL=llama3.2:1b
    ```

### Usage

1. **Run the Streamlit App:**

    ```bash
    streamlit run src/streamlit_app.py
    ```

    This will open a new browser window with the Streamlit interface where you can upload PDF files and view summaries.

2. **Add PDF Files:**

    You can upload your PDF files directly through the web interface.

### Running with Docker

```bash
docker build -t pdf-summarizer:local .
docker run -p 8501:8501 \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=llama3.2:1b \
  pdf-summarizer:local
```

`host.docker.internal` lets the container reach an Ollama instance running on your host machine. The image runs as a non-root user and exposes a health endpoint at `/_stcore/health`.

### Project Structure

- `data/`: Contains raw and processed PDF files.
- `docs/`: Documentation related to the project.
- `src/`: Source code for PDF reading, text processing, summarization, and the Streamlit app.
- `test/`: Unit tests.
- `deploy/environments/`: Per-environment (`dev`/`qa`/`prod`) configuration values, consumed by an external deployment chart.
- `.github/workflows/`: CI pipeline (lint + test).
- `Dockerfile`: Multi-stage, non-root container image.
- `.gitignore`: Specifies files and directories to ignore in Git.
- `requirements.txt`: Pinned Python package dependencies.
- `README.md`: This file.

## Testing

To run tests, use:

```bash
pytest
```

CI runs `ruff` (lint) and `pytest` on every push and pull request.

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
