from __future__ import annotations

import importlib
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.core.config import get_settings
from src.db.session import reset_engine_for_tests

REPO_ROOT = Path(__file__).resolve().parents[3]
PAYLOAD_PATH = REPO_ROOT / "data" / "artifacts" / "research_demo" / "research_demo_payload.json"
TEST_DATA_DIR = REPO_ROOT / ".tmp_api_tests"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = TEST_DATA_DIR / f"platform_{uuid.uuid4().hex}.sqlite"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("RESEARCH_DEMO_PAYLOAD_PATH", str(PAYLOAD_PATH))
    monkeypatch.setenv("AUTO_SEED_FROM_RESEARCH_PAYLOAD", "true")
    get_settings.cache_clear()
    reset_engine_for_tests()

    import src.main as main

    importlib.reload(main)
    with TestClient(main.app) as test_client:
        yield test_client

    get_settings.cache_clear()
    reset_engine_for_tests()


def test_platform_status_and_dashboard(client: TestClient) -> None:
    status = client.get("/api/platform/status")
    assert status.status_code == 200
    assert status.json()["seeded"] is True

    dashboard = client.get("/api/dashboard")
    assert dashboard.status_code == 200
    payload = dashboard.json()
    assert payload["cohort"]["studentCount"] == 120
    assert len(payload["students"]) == 120


def test_student_detail_and_twin_snapshots(client: TestClient) -> None:
    students = client.get("/api/students").json()
    student_id = students[0]["studentId"]

    detail = client.get(f"/api/students/{student_id}")
    assert detail.status_code == 200
    assert detail.json()["studentId"] == student_id
    assert len(detail.json()["timeline"]) == 10

    snapshots = client.get(f"/api/twins/{student_id}/snapshots")
    assert snapshots.status_code == 200
    assert len(snapshots.json()) == 10


def test_predictions_explanations_and_research_evidence(client: TestClient) -> None:
    predictions = client.get("/api/predictions/latest")
    assert predictions.status_code == 200
    assert len(predictions.json()["predictions"]) == 120

    global_xai = client.get("/api/explanations/global")
    assert global_xai.status_code == 200
    assert global_xai.json()["topGlobalFeatures"]

    cases = client.get("/api/explanations/cases")
    assert cases.status_code == 200
    assert len(cases.json()) == 5
    first_case = cases.json()[0]
    assert first_case["studentId"]
    assert first_case["studentLabel"]

    evidence = client.get("/api/research/evidence")
    assert evidence.status_code == 200
    assert evidence.json()["timeline"][0]["id"] == "exp_001"
