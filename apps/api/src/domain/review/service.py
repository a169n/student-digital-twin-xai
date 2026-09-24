from __future__ import annotations

from src.db.models import ReviewDecisionRecord
from src.domain.review.models import DecisionIn
from src.domain.review.repository import ReviewRepository


class CaseNotFound(Exception):
    pass


class FactorNotShown(Exception):
    pass


def source_key(case: dict) -> str:
    """The source student a case points at; decisions are bound to it, not to the pseudonym."""
    return f"{case['source']['cohortId']}:{case['source']['studentRow']}"


def _decision(record: ReviewDecisionRecord) -> dict:
    return {
        "id": record.id,
        "action": record.action,
        "factor": record.factor,
        "note": record.note,
        "createdAt": record.created_at.isoformat() + "Z",
    }


class ReviewService:
    def __init__(self, repository: ReviewRepository) -> None:
        self.repository = repository

    def list_cases(self) -> list[dict]:
        latest: dict[tuple[str, str], dict] = {}
        for record in self.repository.decisions():  # newest first
            latest.setdefault((record.case_id, record.source_key), _decision(record))
        return [
            {
                "caseId": case["caseId"],
                "displayName": case["displayName"],
                "institution": case["institution"],
                "course": case["context"]["course"],
                "risk": case["risk"],
                "flagged": case["flagged"],
                "verdict": case["reliability"]["verdict"],
                "selfTau": case["reliability"]["selfTau"],
                "latestDecision": latest.get((case["caseId"], source_key(case))),
            }
            for case in self.repository.cases()
        ]

    def get_case(self, case_id: str) -> dict:
        case = self.repository.case(case_id)
        if case is None:
            raise CaseNotFound(case_id)
        metadata = self.repository.metadata()
        return {
            "case": case,
            "scaleContext": metadata.get("scaleContext"),
            "featureLabels": metadata.get("featureLabels"),
            "decisions": [
                _decision(r)
                for r in self.repository.decisions(case_id)
                if r.source_key == source_key(case)
            ],
        }

    def record_decision(self, case_id: str, decision: DecisionIn) -> dict:
        case = self.repository.case(case_id)
        if case is None:
            raise CaseNotFound(case_id)
        shown = {f["feature"] for f in case["factors"]}
        if decision.factor is not None and decision.factor not in shown:
            raise FactorNotShown(decision.factor)
        record = self.repository.add_decision(
            case_id, source_key(case), decision.action, decision.factor, decision.note
        )
        return _decision(record)
