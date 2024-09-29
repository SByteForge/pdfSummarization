import pytest
from src.summarizer import generate_summary

def test_summarization_length():
    text = "This is a sample text for summarization."
    summary = generate_summary(text, length=20)
    assert len(summary) <= 20, "Summary exceeds the specified length."

def test_summarization_accuracy():
    text = "This is a simple text meant to test summarization accuracy."
    summary = generate_summary(text)
    assert len(summary) > 0, "Summarization failed to return any text."
