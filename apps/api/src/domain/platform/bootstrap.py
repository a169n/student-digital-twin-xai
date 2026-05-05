from __future__ import annotations

from pathlib import Path

from src.core.config import get_settings
from src.db import init_db
from src.db.session import get_sessionmaker
from src.domain.platform.repository import PlatformRepository
from src.importer.research_payload import ImportSummary, import_research_payload


def initialize_platform_store() -> ImportSummary | None:
    init_db()
    settings = get_settings()
    if not settings.auto_seed_from_research_payload:
        return None

    payload_path = Path(settings.research_demo_payload_path)
    if not payload_path.exists():
        return None

    session_factory = get_sessionmaker()
    with session_factory() as session:
        repository = PlatformRepository(session)
        if repository.count_students() > 0:
            return None
        return import_research_payload(session, payload_path=payload_path)
