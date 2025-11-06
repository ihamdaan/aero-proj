# config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    linkedin_email: str = Field(..., env="LINKEDIN_EMAIL")
    linkedin_password: str = Field(..., env="LINKEDIN_PASSWORD")
    headless: bool = Field(default=False)
    proxy_list_path: str = Field(default="data/proxies.txt")

    class Config:
        env_file = Path(__file__).resolve().parent / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
