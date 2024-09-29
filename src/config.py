import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for application settings."""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    RAW_DATA_PATH = os.path.join('data', 'raw')
    PROCESSED_DATA_PATH = os.path.join('data', 'processed')
    MODEL_NAME = "gpt-3.5-turbo-16k"
    MAX_TOKENS = 150
    DEBUG_MODE = True
