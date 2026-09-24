from __future__ import annotations

from pathlib import Path

from sqlalchemy import select

from src.core.config import get_settings
from src.db import init_db
from src.db.models import ReviewCaseRecord
from src.db.session import get_sessionmaker
from src.domain.platform.repository import PlatformRepository
from src.importer.research_payload import ImportSummary, import_research_payload
from src.importer.review_payload import import_review_payload


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


def initialize_review_store() -> int | None:
    """Load the review payload once, if it exists and nothing is loaded yet.

    Separate from the research seed above, which returns early once students
    exist, so an existing database still picks up review cases.
    """
    init_db()
    payload_path = Path(get_settings().review_payload_path)
    if not payload_path.exists():
        return None
    with get_sessionmaker()() as session:
        if session.scalar(select(ReviewCaseRecord.case_id).limit(1)) is not None:
            return None
        return import_review_payload(session, payload_path=payload_path)
