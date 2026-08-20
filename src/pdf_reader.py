from pypdf import PdfReader

class PDFReader:
    """Class to handle PDF reading."""

    @staticmethod
    def read_pdf(file):
        """Read a PDF file and extract text."""
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
