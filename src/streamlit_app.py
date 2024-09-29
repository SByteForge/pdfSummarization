import streamlit as st
import os
from src.summarizer import Summarizer
from src.config import Config

def main():
    st.set_page_config(page_title="PDF Summarization")
    st.title("PDF Summarization App")
    st.write("Summarize your file within a few seconds")
    st.divider()
    
    pdf = st.file_uploader('Upload your PDF Document', type='pdf')
    submit = st.button("Generate Summary")
    
    os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
    
    if submit:
        if pdf is not None:
            with st.spinner('Generating summary...'):
                try:
                    response = Summarizer.summarize_pdf(pdf)
                    st.subheader('Summary of file:')
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please upload a PDF file.")

if __name__ == '__main__':
    main()
