from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, ReviewCaseRecord, ReviewDecisionRecord, ReviewMetadataRecord
from src.importer.review_payload import import_review_payload
from tests.review_fixtures import write_review_payload

TMP = Path(__file__).resolve().parents[3] / ".tmp_api_tests"


def _session():
    TMP.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{(TMP / f'review_{uuid.uuid4().hex}.sqlite').as_posix()}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_import_loads_cases_in_payload_order_and_metadata():
    session = _session()
    path = TMP / f"payload_{uuid.uuid4().hex}.json"
    write_review_payload(path)
    assert import_review_payload(session, payload_path=path) == 2
    ids = session.scalars(select(ReviewCaseRecord.case_id).order_by(ReviewCaseRecord.position))
    assert list(ids) == ["OU-1", "OU-2"]
    assert session.get(ReviewMetadataRecord, 1) is not None


def test_reimport_replaces_cases_and_keeps_decisions():
    from datetime import datetime

    session = _session()
    path = TMP / f"payload_{uuid.uuid4().hex}.json"
    write_review_payload(path)
    import_review_payload(session, payload_path=path)
    session.add(
        ReviewDecisionRecord(
            case_id="OU-1",
            source_key="oulad_BBB_2013J:7",
            action="keep_monitoring",
            factor=None,
            note=None,
            created_at=datetime(2026, 9, 24),
        )
    )
    session.commit()
    assert import_review_payload(session, payload_path=path) == 2
    assert session.scalar(select(ReviewDecisionRecord.case_id)) == "OU-1"
    assert len(list(session.scalars(select(ReviewCaseRecord)))) == 2
