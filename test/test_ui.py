import streamlit as st
from streamlit.testing import TestSession

def test_file_upload_ui():
    test_session = TestSession()
    with test_session:
        file_uploader = st.file_uploader("Upload PDF", type=["pdf"])
        assert file_uploader is not None, "File upload component failed to load."
