import time
from src.pdf_reader import extract_text_from_pdf
from src.summarizer import generate_summary

def test_pdf_processing_time():
    start_time = time.time()
    text = extract_text_from_pdf("tests/sample_files/sample.pdf")
    summary = generate_summary(text)
    end_time = time.time()

    assert (end_time - start_time) < 10, "PDF processing took too long."
