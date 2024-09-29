# PDF Summarizer

## Overview

The **PDF Summarizer** project is an application designed to read PDF files and generate concise summaries using Large Language Models (LLMs). This project leverages LangChain for language processing and Streamlit for creating an interactive user interface.

## Features

- **PDF Reading**: Extracts text from PDF documents.
- **Summarization**: Uses LLMs to generate summaries of the extracted text.
- **Interactive UI**: Provides a web-based interface with Streamlit for easy interaction.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/pdf-summarizer.git
    cd pdf-summarizer
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment:**

    You may need to configure certain environment variables or API keys depending on the services you use. Create a `.env` file in the root directory and add necessary configuration settings.

### Usage

1. **Add PDF Files:**

    Place your PDF files in the `data/raw` directory.

2. **Run the Streamlit App:**

    Start the Streamlit web application with the following command:

    ```bash
    streamlit run src/streamlit_app.py
    ```

    This will open a new browser window with the Streamlit interface where you can upload PDF files and view summaries.

3. **Configuration:**

    Modify `src/config.py` if you need to adjust any configuration settings or paths.

### Project Structure

- `data/`: Contains raw and processed PDF files.
- `docs/`: Documentation related to the project.
- `src/`: Source code for PDF reading, summarization, and Streamlit app.
- `tests/`: Unit and integration tests.
- `.gitignore`: Specifies files and directories to ignore in Git.
- `requirements.txt`: Python package dependencies.
- `README.md`: This file.
- `setup.py`: Setup script for installing the project as a package.

## Testing

To run tests, use:

```bash
pytest



pdf-summarizer/
│
├── data/
│   ├── raw/                # Store raw PDF files here
│   └── processed/          # Store any processed or intermediate files
│
├── docs/                   # Documentation for your project
│   ├── architecture.md     # Overview of system architecture
│   ├── usage.md            # How to use the project
│   └── api.md              # API documentation if applicable
│
├── src/                    # Source code for your project
│   ├── __init__.py         # Makes src a Python package
│   ├── config.py           # Configuration file for settings
│   ├── pdf_reader.py       # Code to read and extract text from PDF files
│   ├── summarizer.py       # Code to summarize the text using LLMs
│   ├── langchain_utils.py  # LangChain utilities and integrations
│   └── streamlit_app.py    # Streamlit app for user interface
│
├── tests/                  # Unit tests and integration tests
│   ├── __init__.py         # Makes tests a Python package
│   ├── test_pdf_reader.py  # Tests for PDF reading functionality
│   ├── test_summarizer.py  # Tests for summarization functionality
│   ├── test_langchain.py   # Tests for LangChain utilities
│   └── test_streamlit.py   # Tests for Streamlit app
│
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md               # Project overview and instructions
└── setup.py                # Setup script for package installation
