import pytest

from src.exceptions import SummarizationError
from src.openai_client import OpenAIClient


class _FakeKnowledgeBase:
    def similarity_search(self, query):
        return ["doc1", "doc2"]


class _FakeChain:
    def __init__(self, response=None, error=None):
        self._response = response
        self._error = error

    def run(self, **kwargs):
        if self._error:
            raise self._error
        return self._response


def test_summarize_returns_llm_response(monkeypatch):
    monkeypatch.setattr("src.openai_client.ChatOllama", lambda **kwargs: object())
    monkeypatch.setattr(
        "src.openai_client.load_qa_chain",
        lambda llm, chain_type: _FakeChain(response="a generated summary"),
    )

    result = OpenAIClient.summarize(_FakeKnowledgeBase(), "Summarize this.")

    assert result == "a generated summary"


def test_summarize_wraps_failures(monkeypatch):
    monkeypatch.setattr("src.openai_client.ChatOllama", lambda **kwargs: object())
    monkeypatch.setattr(
        "src.openai_client.load_qa_chain",
        lambda llm, chain_type: _FakeChain(error=RuntimeError("ollama unreachable")),
    )

    with pytest.raises(SummarizationError):
        OpenAIClient.summarize(_FakeKnowledgeBase(), "Summarize this.")
