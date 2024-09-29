# API Documentation

## Overview

The PDF Summarizer integrates with OpenAI's API to generate text summaries. This documentation outlines the main components and their interactions.

## Endpoints

### 1. Summarization

- **Endpoint**: OpenAI API (via LangChain)
- **Method**: POST
- **Description**: Takes a set of documents and a query to generate a summary.

#### Request

- **Input**: 
  - `documents`: List of text chunks extracted from the PDF.
  - `question`: A query string asking for a summary of the content.

#### Response

- **Output**: A summary of the provided documents in a user-friendly format.

### Example Usage

In the `summarizer.py` file, the following code demonstrates how the API is called:

```python
response = chain.run(input_documents=docs, question=query)
