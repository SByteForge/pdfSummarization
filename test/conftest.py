import io

import pytest
from pypdf import PdfWriter


def _make_pdf_bytes(page_texts):
    """Build an in-memory PDF with one blank page per entry in page_texts.

    pypdf's writer can't draw text, so pages are blank; extract_text() on a
    blank page returns "". Tests that need real extractable text patch
    PdfReader.extract_text via the `readable_pdf_bytes` monkeypatch fixture
    instead of relying on physically rendered text.
    """
    writer = PdfWriter()
    for _ in page_texts:
        writer.add_blank_page(width=200, height=200)
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer


@pytest.fixture
def blank_pdf_bytes():
    """A minimal, valid, single-page PDF with no extractable text."""
    return _make_pdf_bytes([""])


@pytest.fixture
def multi_page_blank_pdf_bytes():
    """A minimal, valid, three-page PDF with no extractable text."""
    return _make_pdf_bytes(["", "", ""])


@pytest.fixture
def not_a_pdf_bytes():
    """Bytes that are not a valid PDF."""
    return io.BytesIO(b"this is definitely not a pdf file")
