import pytest
from src.pdf_reader import extract_text_from_pdf

def test_pdf_extraction():
    extracted_text = extract_text_from_pdf("tests/sample_files/sample.pdf")
    assert len(extracted_text) > 0, "Text extraction failed for the sample PDF."

def test_multi_page_pdf_extraction():
    extracted_text = extract_text_from_pdf("tests/sample_files/multi_page_sample.pdf")
    assert "Page 1 text" in extracted_text, "Failed to extract text from page 1."
    assert "Page 2 text" in extracted_text, "Failed to extract text from page 2."

def test_empty_pdf():
    extracted_text = extract_text_from_pdf("tests/sample_files/empty.pdf")
    assert extracted_text == "", "Empty PDF should return an empty string."
