# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


# class Settings(BaseSettings):
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL", "postgresql://postgres:anis1234@localhost/bbtdb"
#     )
#     REDIS_HOST: str = os.getenv("REDIS_HOST")
#     REDIS_PORT: int = int(os.getenv("REDIS_PORT"))

#     BITCOMMERZ_TOKEN_URL: str = os.getenv("BITCOMMERZ_TOKEN_URL")
#     BITCOMMERZ_CLIENT_ID: str = os.getenv("BITCOMMERZ_CLIENT_ID")
#     BITCOMMERZ_CLIENT_SECRET: str = os.getenv("BITCOMMERZ_CLIENT_SECRET")
#     REDIRECT_URI: str = os.getenv("REDIRECT_URI")


#     class Config:
#         env_file = ".env"
#         case_sensitive = True
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:anis1234@localhost/bbtdb"
    REDIS_HOST: str
    REDIS_PORT: int

    BITCOMMERZ_TOKEN_URL: str
    BITCOMMERZ_CLIENT_ID: str
    BITCOMMERZ_CLIENT_SECRET: str
    REDIRECT_URI: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
