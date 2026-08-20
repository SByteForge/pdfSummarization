from src.pdf_reader import PDFReader
from src.text_processor import TextProcessor
from src.openai_client import OpenAIClient

class Summarizer:
    """Class to summarize PDF files."""

    @staticmethod
    def summarize_pdf(pdf):
        """Summarize the content of the provided PDF file."""
        if pdf is None:
            raise ValueError("No PDF file provided for summarization.")
        
        text = PDFReader.read_pdf(pdf)
        knowledge_base = TextProcessor.process_text(text)
        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."
        
        return OpenAIClient.summarize(knowledge_base, query)
