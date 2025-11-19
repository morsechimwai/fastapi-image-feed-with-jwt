"""Application configuration settings."""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./image-feed.sqlite3"

    # Security
    SECRET: str

    # ImageKit
    IMAGEKIT_PUBLIC_KEY: str
    IMAGEKIT_PRIVATE_KEY: str
    IMAGEKIT_URL_ENDPOINT: str

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Image Feed Backend"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


settings = Settings()

