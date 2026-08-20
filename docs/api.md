# API Documentation

## Overview

The PDF Summarizer integrates with a locally-hosted LLM via [Ollama](https://ollama.com) to generate text summaries. No external/paid API is used. This documentation outlines the main components and their interactions.

## Configuration

The Ollama integration is configured entirely through environment variables (see `src/config.py`):

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434` | Base URL of the Ollama server |
| `OLLAMA_MODEL` | `llama3.2:1b` | Model name to use for summarization |

## Summarization

- **Backend**: Ollama, called via `langchain-ollama`'s `ChatOllama` (see `src/openai_client.py`)
- **Description**: Takes a set of retrieved document chunks and a query, and returns a generated summary.

### Request

- **Input**:
  - `knowledge_base`: A FAISS vector store built from the PDF's embedded text chunks.
  - `query`: A query string asking for a summary of the content.

### Response

- **Output**: A summary of the provided documents as plain text.

### Example Usage

In `src/openai_client.py`, the following code demonstrates how the local LLM is called:

```python
llm = ChatOllama(base_url=Config.OLLAMA_URL, model=Config.OLLAMA_MODEL, temperature=0.8)
chain = load_qa_chain(llm, chain_type="stuff")
response = chain.run(input_documents=knowledge_base.similarity_search(query), question=query)
```

### Errors

Failures from the Ollama call (e.g. the server being unreachable, or the model not being pulled) are caught and re-raised as `SummarizationError` (see `src/exceptions.py`), which the Streamlit UI surfaces as a user-facing error message rather than a crash.
