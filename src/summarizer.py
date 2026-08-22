import io

from src.exceptions import PDFSummarizerError
from src.openai_client import OpenAIClient
from src.pdf_reader import PDFReader
from src.prompts import DETAILED as DEFAULT_QUERY
from src.storage import PDFStorage
from src.text_processor import TextProcessor


class Summarizer:
    """Class to summarize PDF files."""

    @staticmethod
    def summarize_pdf(pdf, query: str = DEFAULT_QUERY) -> str:
        """Store, then summarize, the content of the provided PDF file.

        The upload is durably stored (S3/LocalStack) before any processing
        happens — if storage fails, the request fails closed and processing
        never starts, since there'd be no durable record of what was
        processed.

        Raises:
            PDFSummarizerError: If no PDF is provided.
            StorageError: If the upload cannot be durably stored.
            PDFExtractionError: If the PDF cannot be read or has no text.
            SummarizationError: If the summarization backend fails.
        """
        if pdf is None:
            raise PDFSummarizerError("No PDF file provided for summarization.")

        data = pdf.read()
        filename = getattr(pdf, "name", "upload.pdf")
        PDFStorage.store(data, filename)

        text = PDFReader.read_pdf(io.BytesIO(data))
        knowledge_base = TextProcessor.process_text(text)

        return OpenAIClient.summarize(knowledge_base, query)
