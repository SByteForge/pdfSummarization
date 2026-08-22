from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.config import Config

APP_PATH = str(Path(__file__).parent.parent / "src" / "streamlit_app.py")


@pytest.fixture(autouse=True)
def _isolated_governance_db(tmp_path, monkeypatch):
    """Keep the app's governance.init_db() call from writing into the real repo during tests."""
    monkeypatch.setattr(Config, "GOVERNANCE_DB_PATH", str(tmp_path / "test_governance.db"))


def test_app_renders_without_crashing():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    assert not at.exception


def test_app_shows_title_and_file_uploader():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    assert at.title[0].value == "PDF Summarization App"
    assert len(at.file_uploader) == 1


def test_app_shows_sidebar_controls():
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=30)
    assert len(at.sidebar.selectbox) == 1
    assert len(at.sidebar.radio) == 1
