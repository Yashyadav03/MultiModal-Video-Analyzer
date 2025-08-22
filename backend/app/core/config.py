from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # DeepSeek API configuration
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()