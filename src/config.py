import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for application settings."""

    RAW_DATA_PATH = os.path.join("data", "raw")
    PROCESSED_DATA_PATH = os.path.join("data", "processed")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    DEBUG_MODE = os.getenv("PDF_SUMMARIZER_DEBUG", "false").lower() == "true"
    GOVERNANCE_DB_PATH = os.getenv("GOVERNANCE_DB_PATH", os.path.join("data", "governance.db"))
