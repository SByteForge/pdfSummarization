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

    # LocalStack S3 — durable storage for uploaded PDFs, written before processing.
    S3_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "pdf-summarizer-documents")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
