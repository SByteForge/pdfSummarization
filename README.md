# PDF Summarizer

## Overview

**PDF Summarizer** is a production-shaped retrieval-augmented generation (RAG) service that summarizes PDF documents end-to-end without a single paid API call. An upload is durably stored (S3-compatible storage via LocalStack) before any processing happens, then extracted, chunked, and embedded locally via `sentence-transformers`, indexed in FAISS for semantic retrieval, and summarized by a self-hosted LLM served through [Ollama](https://ollama.com) — free to run, private by default, and portable to any environment with a CPU or GPU. Every retrieval and generation call is governed: audited to a local store, rate-limited per session, and surfaced on a dedicated Cost Dashboard alongside illustrative per-call cost estimates. The service is packaged as a multi-stage, non-root Docker image and validated through a GitHub Actions CI pipeline.

## Features

- **Durable storage first**: uploads are written to S3-compatible storage (LocalStack) before processing — if storage fails, the request fails closed rather than silently processing an unpersisted file.
- **Local retrieval**: chunks and embeds text locally (`sentence-transformers`) and indexes it with FAISS.
- **Local summarization**: uses a self-hosted LLM via Ollama to generate structured summaries — no data leaves your machine.
- **Governance**: every retrieval and generation call is audited (SQLite), with enforced policies (query length limits, per-session rate limiting).
- **Cost Dashboard**: a dedicated page showing token usage, illustrative cost estimates, and the full audit trail.
- **Interactive UI**: staged pipeline visibility, model/detail-level controls, streaming output, and a pre-flight health check.
- **Containerized**: ships with a multi-stage, non-root Dockerfile.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Pip (Python package installer)
- [Ollama](https://ollama.com) installed and running, with a model pulled (default: `llama3.2:1b`)
- A LocalStack (or other S3-compatible) endpoint reachable — storage is a hard dependency, not optional: uploads are stored before processing, and the request fails if storage is unreachable

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

    The app talks to Ollama over `OLLAMA_URL` (default `http://localhost:11434`) and uses `OLLAMA_MODEL` (default `llama3.2:1b`), and to S3-compatible storage over `AWS_ENDPOINT_URL` (default `http://localhost:4566`, LocalStack's default port). Override any of these in a `.env` file if needed:

    ```plaintext
    OLLAMA_URL=http://localhost:11434
    OLLAMA_MODEL=llama3.2:1b
    AWS_ENDPOINT_URL=http://localhost:4566
    AWS_ACCESS_KEY_ID=test
    AWS_SECRET_ACCESS_KEY=test
    S3_BUCKET_NAME=pdf-summarizer-documents
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
  -e AWS_ENDPOINT_URL=http://host.docker.internal:4566 \
  pdf-summarizer:local
```

`host.docker.internal` lets the container reach Ollama and LocalStack running on your host machine (or reachable via a `kubectl port-forward`, if you're pointing at a platform-hosted LocalStack). The image runs as a non-root user and exposes a health endpoint at `/_stcore/health`.

### Project Structure

- `data/`: Contains raw and processed PDF files.
- `docs/`: Documentation related to the project.
- `src/`: Source code.
  - `pdf_reader.py`, `text_processor.py`, `openai_client.py` (Ollama-backed), `summarizer.py`: the RAG pipeline.
  - `storage.py`: durable PDF storage (S3/LocalStack), written before processing.
  - `governance.py`: audit logging and policy enforcement for retrieval and generation.
  - `health.py`, `prompts.py`, `config.py`, `exceptions.py`: supporting modules.
  - `streamlit_app.py`: the main UI.
  - `pages/`: additional Streamlit pages (Cost Dashboard).
- `test/`: Unit tests.
- `deploy/environments/`: Per-environment (`dev`/`qa`/`prod`) configuration values, consumed by an external deployment chart.
- `.github/workflows/`: CI pipeline (lint + test).
- `.streamlit/config.toml`: Streamlit server config (upload size limit).
- `Dockerfile`: Multi-stage, non-root container image.
- `.gitignore`: Specifies files and directories to ignore in Git.
- `requirements.txt`: Pinned Python package dependencies.
- `LICENSE`: MIT License.
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
