import logging

from langchain.chains.question_answering import load_qa_chain
from langchain_ollama import ChatOllama

from src.config import Config
from src.exceptions import SummarizationError

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Class to interact with the local LLM (via Ollama) for summarization."""

    @staticmethod
    def summarize(knowledge_base, query: str) -> str:
        """Generate a summary using a local Ollama model.

        Raises:
            SummarizationError: If the underlying LLM call fails.
        """
        llm = ChatOllama(base_url=Config.OLLAMA_URL, model=Config.OLLAMA_MODEL, temperature=0.8)
        chain = load_qa_chain(llm, chain_type="stuff")

        try:
            response = chain.run(
                input_documents=knowledge_base.similarity_search(query), question=query
            )
            return response
        except Exception as exc:
            raise SummarizationError(f"Failed to generate summary: {exc}") from exc
