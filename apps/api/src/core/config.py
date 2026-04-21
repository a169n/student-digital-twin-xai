from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "student-digital-twin-xai-api"
    app_env: str = "development"
    api_port: int = 8000
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/sdtxai"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
