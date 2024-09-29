import streamlit as st 
import os
from utils import *

def main():
    st.set_page_config(page_title="PDF Summarize")
    
    st.title("PDF Summrization App")
    st.write("Summarize your file within few seconds")
    st.divider()
    
    
    pdf=st.file_uploader('Upload your PDF Document', type='PDF')
    
    submit=st.button("Genrate Summary")
    os.environ["OPENAI_API_KEY"]="enter you key"
    
    if submit:
        reponse=summarizer(pdf)
        st.subheader('Summary of file:')
        st.write(reponse)
    
if __name__== '__main__':
    main()

