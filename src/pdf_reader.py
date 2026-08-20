import logging

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from src.exceptions import PDFExtractionError

logger = logging.getLogger(__name__)


class PDFReader:
    """Class to handle PDF reading."""

    @staticmethod
    def read_pdf(file) -> str:
        """Read a PDF file and extract its text.

        Args:
            file: A file path or file-like object pointing to a PDF.

        Returns:
            The concatenated text of all pages.

        Raises:
            PDFExtractionError: If the file cannot be parsed as a PDF or
                contains no extractable text.
        """
        try:
            pdf_reader = PdfReader(file)
        except PdfReadError as exc:
            raise PDFExtractionError(f"Could not read file as a PDF: {exc}") from exc

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            logger.warning("No extractable text found in PDF %r", file)
            raise PDFExtractionError(
                "No extractable text found in this PDF. It may be a scanned "
                "image without an OCR text layer."
            )

        return text
