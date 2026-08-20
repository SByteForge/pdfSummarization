import logging

import streamlit as st

from src.config import Config
from src.exceptions import PDFSummarizerError
from src.summarizer import Summarizer

logging.basicConfig(level=logging.DEBUG if Config.DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)


def main():
    st.set_page_config(page_title="PDF Summarization")
    st.title("PDF Summarization App")
    st.write("Summarize your file within a few seconds")
    st.divider()

    pdf = st.file_uploader("Upload your PDF Document", type="pdf")
    submit = st.button("Generate Summary")

    if submit:
        if pdf is not None:
            with st.spinner("Generating summary..."):
                try:
                    response = Summarizer.summarize_pdf(pdf)
                    st.subheader("Summary of file:")
                    st.write(response)
                except PDFSummarizerError as e:
                    logger.warning("Summarization failed: %s", e)
                    st.error(str(e))
                except Exception:
                    logger.exception("Unexpected error while summarizing PDF")
                    st.error("An unexpected error occurred while generating the summary.")
        else:
            st.error("Please upload a PDF file.")


if __name__ == "__main__":
    main()
