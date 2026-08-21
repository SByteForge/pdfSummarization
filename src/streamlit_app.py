import logging
import time

import streamlit as st

from src.config import Config
from src.exceptions import PDFExtractionError, SummarizationError
from src.health import check_ollama
from src.openai_client import OpenAIClient
from src.pdf_reader import PDFReader
from src.prompts import DEFAULT_LEVEL, PROMPTS
from src.text_processor import TextProcessor

logging.basicConfig(level=logging.DEBUG if Config.DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)


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

    return model, level


def render_pipeline(pdf, model: str, query: str):
    """Run the pipeline with visible stages, returning (summary, documents, timings)."""
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
    status.update(label=f"Generating summary with {model}...")

    t0 = time.perf_counter()
    summary = st.write_stream(OpenAIClient.summarize_stream(documents, query, model=model))
    timings["generate"] = time.perf_counter() - t0

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
            summary, documents, timings = render_pipeline(pdf, model, query)
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
