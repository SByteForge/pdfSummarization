import pytest

from src.exceptions import PDFExtractionError
from src.pdf_reader import PDFReader


def test_invalid_pdf_upload(not_a_pdf_bytes):
    with pytest.raises(PDFExtractionError):
        PDFReader.read_pdf(not_a_pdf_bytes)


def test_empty_pdf_raises(blank_pdf_bytes):
    with pytest.raises(PDFExtractionError):
        PDFReader.read_pdf(blank_pdf_bytes)
