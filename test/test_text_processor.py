import pytest

from src.exceptions import PDFExtractionError
from src.text_processor import TextProcessor


def test_process_text_rejects_empty_string():
    with pytest.raises(PDFExtractionError):
        TextProcessor.process_text("")


def test_process_text_rejects_whitespace_only():
    with pytest.raises(PDFExtractionError):
        TextProcessor.process_text("   \n\t  ")


def test_process_text_builds_knowledge_base(monkeypatch):
    calls = {}

    class _FakeEmbeddings:
        def __init__(self, model_name):
            calls["model_name"] = model_name

    class _FakeFAISS:
        @staticmethod
        def from_texts(chunks, embeddings):
            calls["chunks"] = chunks
            return "fake-knowledge-base"

    monkeypatch.setattr("src.text_processor.HuggingFaceEmbeddings", _FakeEmbeddings)
    monkeypatch.setattr("src.text_processor.FAISS", _FakeFAISS)

    result = TextProcessor.process_text("Paragraph one.\nParagraph two.")

    assert result == "fake-knowledge-base"
    assert calls["chunks"]
    assert calls["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"
