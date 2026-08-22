import pytest

from src.exceptions import SummarizationError
from src.openai_client import OpenAIClient


class _FakeKnowledgeBase:
    def similarity_search(self, query, k=None):
        return ["doc1", "doc2"]


class _FakeDocument:
    def __init__(self, content):
        self.page_content = content


class _FakeChunk:
    def __init__(self, content):
        self.content = content


class _FakeStreamingLLM:
    def __init__(self, chunks):
        self._chunks = chunks

    def stream(self, prompt):
        return iter(_FakeChunk(c) for c in self._chunks)


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


def test_retrieve_passes_k_through(monkeypatch):
    captured = {}

    class _KB:
        def similarity_search(self, query, k=None):
            captured["query"] = query
            captured["k"] = k
            return ["doc1"]

    result = OpenAIClient.retrieve(_KB(), "Summarize this.", k=5)

    assert result == ["doc1"]
    assert captured == {"query": "Summarize this.", "k": 5}


def test_summarize_stream_yields_content_chunks(monkeypatch):
    monkeypatch.setattr(
        "src.openai_client.ChatOllama",
        lambda **kwargs: _FakeStreamingLLM(["Hello", ", ", "world."]),
    )

    docs = [_FakeDocument("some context")]
    chunks = list(OpenAIClient.summarize_stream(docs, "Summarize this."))

    assert chunks == ["Hello", ", ", "world."]


def test_summarize_stream_wraps_failures(monkeypatch):
    class _FailingLLM:
        def stream(self, prompt):
            raise RuntimeError("ollama unreachable")

    monkeypatch.setattr("src.openai_client.ChatOllama", lambda **kwargs: _FailingLLM())

    docs = [_FakeDocument("some context")]
    with pytest.raises(SummarizationError):
        list(OpenAIClient.summarize_stream(docs, "Summarize this."))
