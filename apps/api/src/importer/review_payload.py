from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.db.models import ReviewCaseRecord, ReviewMetadataRecord

METADATA_KEYS = ("schemaVersion", "generatedFrom", "selectionRule", "scaleContext", "featureLabels")


def import_review_payload(session: Session, *, payload_path: str | Path) -> int:
    """Replace the review cases with the frozen payload's; decisions are left untouched."""
    payload = json.loads(Path(payload_path).read_text(encoding="utf-8"))
    session.execute(delete(ReviewCaseRecord))
    session.execute(delete(ReviewMetadataRecord))
    session.add(
        ReviewMetadataRecord(id=1, payload_json=json.dumps({k: payload[k] for k in METADATA_KEYS}))
    )
    for position, case in enumerate(payload["cases"]):
        session.add(
            ReviewCaseRecord(
                case_id=case["caseId"],
                institution=case["institution"],
                position=position,
                payload_json=json.dumps(case),
            )
        )
    session.commit()
    return len(payload["cases"])
