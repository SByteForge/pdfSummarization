import pytest

from src.exceptions import PDFSummarizerError
from src.summarizer import Summarizer


def test_summarize_pdf_raises_without_a_file():
    with pytest.raises(PDFSummarizerError):
        Summarizer.summarize_pdf(None)


def test_summarize_pdf_orchestrates_pipeline(monkeypatch):
    monkeypatch.setattr("src.summarizer.PDFReader.read_pdf", lambda pdf: "extracted text")
    monkeypatch.setattr("src.summarizer.TextProcessor.process_text", lambda text: "fake-kb")

    captured = {}

    def fake_summarize(knowledge_base, query):
        captured["knowledge_base"] = knowledge_base
        captured["query"] = query
        return "a short summary"

    monkeypatch.setattr("src.summarizer.OpenAIClient.summarize", fake_summarize)

    result = Summarizer.summarize_pdf(object())

    assert result == "a short summary"
    assert captured["knowledge_base"] == "fake-kb"
    assert "summar" in captured["query"].lower()
