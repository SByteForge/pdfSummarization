import pytest
from src.pdf_reader import extract_text_from_pdf
import os

def test_invalid_pdf_upload():
    with pytest.raises(Exception, match="Invalid PDF format"):
        extract_text_from_pdf("tests/sample_files/invalid_file.txt")

def test_api_key_missing(monkeypatch):
    original_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = ""  # Temporarily unset API key
    
    from src.summarizer import generate_summary
    with pytest.raises(Exception, match="API key is missing"):
        generate_summary("Test text")

    os.environ["OPENAI_API_KEY"] = original_key  # Reset API key
