from __future__ import annotations

import json
from pathlib import Path


def _case(case_id: str, verdict: str, student_row: int = 7) -> dict:
    factors = [
        {
            "feature": "cum_active_days",
            "label": "Active days so far",
            "value": 4.0,
            "courseMedian": 9.0,
            "direction": "raises_risk",
            "share": 0.41,
        },
        {
            "feature": "cum_clicks",
            "label": "Total clicks so far",
            "value": 120.0,
            "courseMedian": 410.0,
            "direction": "raises_risk",
            "share": 0.3,
        },
        {
            "feature": "cum_social",
            "label": "Forum activity so far",
            "value": 3.0,
            "courseMedian": 1.0,
            "direction": "lowers_risk",
            "share": 0.1,
        },
    ]
    return {
        "caseId": case_id,
        "displayName": f"Student {case_id}",
        "institution": "OULAD",
        "source": {"cohortId": "oulad_BBB_2013J", "studentRow": student_row},
        "context": {
            "course": "BBB",
            "week": 13,
            "nWeeks": 39,
            "cohortSize": 2237,
            "passRate": 0.48,
            "modelAuc": 0.85,
        },
        "risk": 0.72,
        "riskRankPct": 0.9,
        "flagged": True,
        "factors": factors,
        "reliability": {
            "selfTau": 0.62 if verdict == "unstable" else 0.9,
            "threshold": 0.8,
            "verdict": verdict,
            "recomputations": [
                {"feature": "cum_active_days", "label": "Active days so far", "count": 5}
            ],
        },
        "features": [
            {k: f[k] for k in ("feature", "label", "value", "courseMedian")} for f in factors
        ],
    }


def write_review_payload(path: Path, ou1_row: int = 7) -> dict:
    payload = {
        "schemaVersion": "teacher_review_v1",
        "generatedFrom": {"experiment": "test"},
        "selectionRule": "test",
        "scaleContext": {
            "threshold": 0.8,
            "coverage": 0.56,
            "retainedAgreement": 0.41,
            "noGateAgreement": 0.35,
            "source": "test",
        },
        "featureLabels": {"cum_active_days": "Active days so far"},
        "cases": [_case("OU-1", "stable", ou1_row), _case("OU-2", "unstable")],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return payload
