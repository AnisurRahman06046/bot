# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:anis1234@localhost/bbtdb"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
