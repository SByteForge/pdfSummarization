import io

import pytest

from src.exceptions import PDFExtractionError
from src.pdf_reader import PDFReader


class _FakePage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class _FakePdfReader:
    def __init__(self, pages_text):
        self.pages = [_FakePage(t) for t in pages_text]


def test_read_pdf_concatenates_all_pages(monkeypatch):
    monkeypatch.setattr(
        "src.pdf_reader.PdfReader", lambda file: _FakePdfReader(["Page one. ", "Page two."])
    )
    text = PDFReader.read_pdf(io.BytesIO(b"irrelevant"))
    assert text == "Page one. Page two."


def test_read_pdf_handles_pages_with_no_text(monkeypatch):
    monkeypatch.setattr(
        "src.pdf_reader.PdfReader", lambda file: _FakePdfReader(["Real text.", None])
    )
    text = PDFReader.read_pdf(io.BytesIO(b"irrelevant"))
    assert text == "Real text."


def test_read_pdf_raises_on_blank_pdf(blank_pdf_bytes):
    with pytest.raises(PDFExtractionError):
        PDFReader.read_pdf(blank_pdf_bytes)


def test_read_pdf_raises_on_invalid_file(not_a_pdf_bytes):
    with pytest.raises(PDFExtractionError):
        PDFReader.read_pdf(not_a_pdf_bytes)
