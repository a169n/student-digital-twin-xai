from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import ReviewCaseRecord, ReviewDecisionRecord, ReviewMetadataRecord


class ReviewRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def cases(self) -> list[dict]:
        rows = self.session.scalars(select(ReviewCaseRecord).order_by(ReviewCaseRecord.position))
        return [json.loads(r.payload_json) for r in rows]

    def case(self, case_id: str) -> dict | None:
        row = self.session.get(ReviewCaseRecord, case_id)
        return json.loads(row.payload_json) if row else None

    def metadata(self) -> dict:
        row = self.session.get(ReviewMetadataRecord, 1)
        return json.loads(row.payload_json) if row else {}

    def decisions(self, case_id: str | None = None) -> list[ReviewDecisionRecord]:
        query = select(ReviewDecisionRecord).order_by(
            ReviewDecisionRecord.created_at.desc(), ReviewDecisionRecord.id.desc()
        )
        if case_id is not None:
            query = query.where(ReviewDecisionRecord.case_id == case_id)
        return list(self.session.scalars(query))

    def add_decision(
        self, case_id: str, source_key: str, action: str, factor: str | None, note: str | None
    ) -> ReviewDecisionRecord:
        record = ReviewDecisionRecord(
            case_id=case_id,
            source_key=source_key,
            action=action,
            factor=factor,
            note=note,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        self.session.add(record)
        self.session.commit()
        return record
