import io

import pytest

from src.exceptions import PDFSummarizerError, StorageError
from src.summarizer import Summarizer


def _fake_pdf(content=b"%PDF-fake", name="upload.pdf"):
    f = io.BytesIO(content)
    f.name = name
    return f


def test_summarize_pdf_raises_without_a_file():
    with pytest.raises(PDFSummarizerError):
        Summarizer.summarize_pdf(None)


def test_summarize_pdf_orchestrates_pipeline(monkeypatch):
    stored = {}
    monkeypatch.setattr(
        "src.summarizer.PDFStorage.store",
        lambda data, filename: stored.update(data=data, filename=filename) or "some-key",
    )
    monkeypatch.setattr("src.summarizer.PDFReader.read_pdf", lambda pdf: "extracted text")
    monkeypatch.setattr("src.summarizer.TextProcessor.process_text", lambda text: "fake-kb")

    captured = {}

    def fake_summarize(knowledge_base, query):
        captured["knowledge_base"] = knowledge_base
        captured["query"] = query
        return "a short summary"

    monkeypatch.setattr("src.summarizer.OpenAIClient.summarize", fake_summarize)

    result = Summarizer.summarize_pdf(_fake_pdf(b"hello", "doc.pdf"))

    assert result == "a short summary"
    assert captured["knowledge_base"] == "fake-kb"
    assert "summar" in captured["query"].lower()
    assert stored == {"data": b"hello", "filename": "doc.pdf"}


def test_summarize_pdf_fails_closed_when_storage_fails(monkeypatch):
    def _raise(data, filename):
        raise StorageError("LocalStack unreachable")

    monkeypatch.setattr("src.summarizer.PDFStorage.store", _raise)
    read_pdf_called = []
    monkeypatch.setattr(
        "src.summarizer.PDFReader.read_pdf", lambda pdf: read_pdf_called.append(True)
    )

    with pytest.raises(StorageError):
        Summarizer.summarize_pdf(_fake_pdf())

    assert read_pdf_called == []  # processing must never start if storage failed
