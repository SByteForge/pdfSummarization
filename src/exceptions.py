"""Custom exceptions for the PDF Summarizer application."""


class PDFSummarizerError(Exception):
    """Base class for all application-specific errors."""


class PDFExtractionError(PDFSummarizerError):
    """Raised when a PDF file cannot be read or contains no extractable text."""


class SummarizationError(PDFSummarizerError):
    """Raised when the summarization backend fails to produce a summary."""


class StorageError(PDFSummarizerError):
    """Raised when the uploaded PDF cannot be durably stored."""
