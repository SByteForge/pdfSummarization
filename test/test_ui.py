from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).parent.parent / "src" / "streamlit_app.py")


def test_app_renders_without_crashing():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    assert not at.exception


def test_app_shows_title_and_file_uploader():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    assert at.title[0].value == "PDF Summarization App"
    assert len(at.file_uploader) == 1
