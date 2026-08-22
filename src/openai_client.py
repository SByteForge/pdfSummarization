import logging
from collections.abc import Iterator

from langchain.chains.question_answering import load_qa_chain
from langchain_ollama import ChatOllama

from src.config import Config
from src.exceptions import SummarizationError

logger = logging.getLogger(__name__)

RETRIEVAL_K = 8


def _build_stuffed_prompt(documents, query: str) -> str:
    """Combine retrieved chunks and the query into a single prompt.

    Mirrors LangChain's "stuff" chain_type prompt shape, kept explicit here so
    the streaming path doesn't depend on internal chain prompt formatting.
    """
    context = "\n\n".join(doc.page_content for doc in documents)
    return (
        "Use the following context from the document to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )


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

    @staticmethod
    def retrieve(knowledge_base, query: str, k: int = RETRIEVAL_K):
        """Return the chunks that would be fed to the model for this query."""
        return knowledge_base.similarity_search(query, k=k)

    @staticmethod
    def summarize_stream(documents, query: str, model: str | None = None) -> Iterator[str]:
        """Stream a summary token-by-token for already-retrieved documents.

        Raises:
            SummarizationError: If the underlying LLM call fails.
        """
        llm = ChatOllama(
            base_url=Config.OLLAMA_URL, model=model or Config.OLLAMA_MODEL, temperature=0.8
        )
        prompt = _build_stuffed_prompt(documents, query)

        try:
            for chunk in llm.stream(prompt):
                if chunk.content:
                    yield chunk.content
        except Exception as exc:
            raise SummarizationError(f"Failed to generate summary: {exc}") from exc
