from src.exceptions import PDFSummarizerError
from src.openai_client import OpenAIClient
from src.pdf_reader import PDFReader
from src.prompts import DETAILED as DEFAULT_QUERY
from src.text_processor import TextProcessor


class Summarizer:
    """Class to summarize PDF files."""

    @staticmethod
    def summarize_pdf(pdf, query: str = DEFAULT_QUERY) -> str:
        """Summarize the content of the provided PDF file.

        Raises:
            PDFSummarizerError: If no PDF is provided, or if extraction /
                summarization fails downstream.
        """
        if pdf is None:
            raise PDFSummarizerError("No PDF file provided for summarization.")

        text = PDFReader.read_pdf(pdf)
        knowledge_base = TextProcessor.process_text(text)

        return OpenAIClient.summarize(knowledge_base, query)
