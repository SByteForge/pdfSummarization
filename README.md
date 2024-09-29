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

4. **Set up your environment:**

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key_here
    ```

### Usage

1. **Run the Streamlit App:**

    Start the Streamlit web application with the following command:

    ```bash
    streamlit run src/streamlit_app.py
    ```

    This will open a new browser window with the Streamlit interface where you can upload PDF files and view summaries.

2. **Add PDF Files:**

    You can upload your PDF files directly through the web interface.

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
```


## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.