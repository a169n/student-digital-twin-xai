from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[4]


def _default_database_url() -> str:
    db_path = REPO_ROOT / "data" / "application" / "research_platform.sqlite"
    return f"sqlite:///{db_path.as_posix()}"


class Settings(BaseSettings):
    app_name: str = "student-digital-twin-xai-api"
    app_env: str = "development"
    api_port: int = 8000
    database_url: str = _default_database_url()
    auto_seed_from_research_payload: bool = True
    research_demo_payload_path: str = str(
        REPO_ROOT / "data" / "artifacts" / "research_demo" / "research_demo_payload.json"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
