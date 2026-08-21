import logging
import time
import uuid

import streamlit as st

from src import governance
from src.config import Config
from src.exceptions import PDFExtractionError, SummarizationError
from src.health import check_ollama
from src.openai_client import OpenAIClient
from src.pdf_reader import PDFReader
from src.prompts import DEFAULT_LEVEL, PROMPTS
from src.text_processor import TextProcessor

logging.basicConfig(level=logging.DEBUG if Config.DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)


def get_session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]


def render_sidebar(health: dict) -> tuple[str, str]:
    st.sidebar.header("Settings")

    if health["reachable"]:
        st.sidebar.success(f"Ollama connected ({len(health['models'])} model(s) pulled)")
    else:
        st.sidebar.error("Ollama unreachable")
        st.sidebar.caption(
            "Check that Ollama is running and reachable at "
            f"`{Config.OLLAMA_URL}` before generating a summary."
        )

    model_options = health["models"] or [Config.OLLAMA_MODEL]
    default_index = model_options.index(Config.OLLAMA_MODEL) if Config.OLLAMA_MODEL in model_options else 0
    model = st.sidebar.selectbox("Model", options=model_options, index=default_index)

    level_options = list(PROMPTS.keys())
    level = st.sidebar.radio(
        "Summary detail",
        options=level_options,
        index=level_options.index(DEFAULT_LEVEL),
        help="Concise: a few sentences. Standard: one paragraph. Detailed: structured, multi-section.",
    )

    st.sidebar.caption("See the **Cost Dashboard** page for the full audit trail and cost estimates.")

    return model, level


def render_pipeline(pdf, model: str, query: str, session_id: str):
    """Run the pipeline with visible stages, logging retrieval and generation for governance."""
    timings = {}
    status = st.status("Extracting text from PDF...", expanded=True)

    t0 = time.perf_counter()
    text = PDFReader.read_pdf(pdf)
    timings["extract"] = time.perf_counter() - t0
    status.update(label="Embedding and indexing chunks...")

    t0 = time.perf_counter()
    knowledge_base = TextProcessor.process_text(text)
    timings["embed"] = time.perf_counter() - t0
    status.update(label="Retrieving relevant context...")

    t0 = time.perf_counter()
    documents = OpenAIClient.retrieve(knowledge_base, query)
    timings["retrieve"] = time.perf_counter() - t0
    governance.log_retrieval(session_id, query, len(documents), timings["retrieve"])
    status.update(label=f"Generating summary with {model}...")

    input_text = "\n\n".join(doc.page_content for doc in documents) + query
    input_tokens = governance.estimate_tokens(input_text)

    t0 = time.perf_counter()
    try:
        summary = st.write_stream(OpenAIClient.summarize_stream(documents, query, model=model))
    except SummarizationError as e:
        governance.log_generation(
            session_id, query, model, input_tokens, 0, time.perf_counter() - t0, success=False, error=str(e)
        )
        raise
    timings["generate"] = time.perf_counter() - t0

    output_tokens = governance.estimate_tokens(summary)
    governance.log_generation(
        session_id, query, model, input_tokens, output_tokens, timings["generate"], success=True
    )

    status.update(label="Done", state="complete", expanded=False)
    return summary, documents, timings


def render_pipeline_details(documents, timings: dict):
    with st.expander("How this summary was generated"):
        cols = st.columns(4)
        cols[0].metric("Extract", f"{timings['extract']:.2f}s")
        cols[1].metric("Embed + index", f"{timings['embed']:.2f}s")
        cols[2].metric("Retrieve", f"{timings['retrieve']:.2f}s")
        cols[3].metric("Generate", f"{timings['generate']:.2f}s")

        st.caption(f"{len(documents)} chunk(s) retrieved and sent to the model:")
        for i, doc in enumerate(documents, start=1):
            preview = doc.page_content[:200].replace("\n", " ")
            st.text(f"[{i}] {preview}{'...' if len(doc.page_content) > 200 else ''}")


def main():
    st.set_page_config(page_title="PDF Summarization", page_icon="📄", layout="wide")
    governance.init_db()
    session_id = get_session_id()

    st.title("PDF Summarization App")
    st.write("Summarize a PDF locally — no external API calls, powered by Ollama.")
    st.divider()

    health = check_ollama()
    model, level = render_sidebar(health)
    query = PROMPTS[level]

    pdf = st.file_uploader("Upload your PDF Document", type="pdf")
    submit = st.button("Generate Summary", disabled=not health["reachable"])

    if submit:
        if pdf is None:
            st.error("Please upload a PDF file.")
            return

        try:
            governance.check_query_policy(query)
            governance.check_rate_limit(session_id)
        except governance.GovernanceError as e:
            st.error(f"Request blocked by governance policy: {e}")
            return

        try:
            summary, documents, timings = render_pipeline(pdf, model, query, session_id)
            st.subheader("Summary of file:")
            st.write(summary)
            render_pipeline_details(documents, timings)
        except PDFExtractionError as e:
            logger.warning("PDF extraction failed: %s", e)
            st.error(f"Couldn't read this PDF: {e}")
        except SummarizationError as e:
            logger.warning("Summarization failed: %s", e)
            st.error(f"Summarization backend failed: {e}. Check that Ollama is running and the model is pulled.")
        except Exception:
            logger.exception("Unexpected error while summarizing PDF")
            st.error("An unexpected error occurred while generating the summary.")


if __name__ == "__main__":
    main()
