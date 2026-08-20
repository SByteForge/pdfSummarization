from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS

class TextProcessor:
    """Class to process text into chunks and create a knowledge base."""

    @staticmethod
    def process_text(text):
        """Process the given text into manageable chunks."""
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        knowledgebase = FAISS.from_texts(chunks, embeddings)
        return knowledgebase
