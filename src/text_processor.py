import logging

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

from src.exceptions import PDFExtractionError

logger = logging.getLogger(__name__)

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class TextProcessor:
    """Class to process text into chunks and create a knowledge base."""

    @staticmethod
    def process_text(text: str) -> FAISS:
        """Split text into chunks and embed them into a searchable FAISS index.

        Raises:
            PDFExtractionError: If there is no text to process.
        """
        if not text or not text.strip():
            raise PDFExtractionError("Cannot process empty text into a knowledge base.")

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        logger.info("Split text into %d chunk(s)", len(chunks))

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        knowledgebase = FAISS.from_texts(chunks, embeddings)
        return knowledgebase
