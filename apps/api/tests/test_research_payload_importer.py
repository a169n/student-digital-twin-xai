from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base
from src.domain.platform.repository import PlatformRepository
from src.importer.research_payload import import_research_payload

REPO_ROOT = Path(__file__).resolve().parents[3]
PAYLOAD_PATH = REPO_ROOT / "data" / "artifacts" / "research_demo" / "research_demo_payload.json"
TEST_DATA_DIR = REPO_ROOT / ".tmp_api_tests"


def test_importer_builds_sqlite_projection() -> None:
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = TEST_DATA_DIR / f"platform_{uuid.uuid4().hex}.sqlite"
    engine = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    with Session() as session:
        summary = import_research_payload(session, payload_path=PAYLOAD_PATH)
        repository = PlatformRepository(session)
        status = repository.status()
        dashboard = repository.dashboard()

    assert summary.student_count == 120
    assert summary.snapshot_count == 1200
    assert summary.explanation_case_count == 5
    assert status["seeded"] is True
    assert status["payloadSchemaVersion"] == "1.0.0"
    assert dashboard["cohort"]["studentCount"] == 120
    assert dashboard["students"][0]["studentId"].startswith("student_")
