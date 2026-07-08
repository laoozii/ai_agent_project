import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    DATA_DIR = os.getenv("DATA_DIR", "data")

    def validate_required(self):
        if not self.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is not set in the environment variables.")
        if not self.MODEL_NAME:
            raise ValueError("MODEL_NAME is not set in the environment variables.")
        
settings = Settings()
