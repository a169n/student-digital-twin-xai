from __future__ import annotations

import importlib
import json
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.core.config import get_settings
from src.db.session import reset_engine_for_tests
from tests.review_fixtures import write_review_payload

REPO_ROOT = Path(__file__).resolve().parents[3]
TMP = REPO_ROOT / ".tmp_api_tests"


def _client(monkeypatch: pytest.MonkeyPatch, with_payload: bool, run: str = "") -> TestClient:
    TMP.mkdir(parents=True, exist_ok=True)
    run = run or uuid.uuid4().hex
    payload = TMP / f"review_{run}.json"
    if with_payload:
        write_review_payload(payload)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(TMP / f'review_{run}.sqlite').as_posix()}")
    monkeypatch.setenv("AUTO_SEED_FROM_RESEARCH_PAYLOAD", "false")
    monkeypatch.setenv("REVIEW_PAYLOAD_PATH", str(payload))
    get_settings.cache_clear()
    reset_engine_for_tests()
    import src.main as main

    importlib.reload(main)
    return TestClient(main.app)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    with _client(monkeypatch, with_payload=True) as c:
        yield c
    get_settings.cache_clear()
    reset_engine_for_tests()


def test_list_cases(client: TestClient) -> None:
    rows = client.get("/api/review/cases").json()
    assert [r["caseId"] for r in rows] == ["OU-1", "OU-2"]
    assert rows[1]["verdict"] == "unstable" and rows[0]["latestDecision"] is None


def test_get_case_with_context(client: TestClient) -> None:
    body = client.get("/api/review/cases/OU-2").json()
    assert body["case"]["caseId"] == "OU-2"
    assert body["scaleContext"]["threshold"] == 0.8
    assert body["decisions"] == []


def test_record_decision_and_see_it_newest_first(client: TestClient) -> None:
    first = client.post("/api/review/cases/OU-1/decisions", json={"action": "keep_monitoring"})
    assert first.status_code == 201
    second = client.post(
        "/api/review/cases/OU-1/decisions",
        json={"action": "factor_looks_wrong", "factor": "cum_clicks", "note": "  "},
    )
    assert second.status_code == 201 and second.json()["note"] is None
    body = client.get("/api/review/cases/OU-1").json()
    assert [d["action"] for d in body["decisions"]] == ["factor_looks_wrong", "keep_monitoring"]
    listed = client.get("/api/review/cases").json()[0]
    assert listed["latestDecision"]["action"] == "factor_looks_wrong"


def test_unknown_case_is_404(client: TestClient) -> None:
    got = client.get("/api/review/cases/XX-9")
    assert got.status_code == 404 and got.json()["detail"] == "Case not found"
    post = client.post("/api/review/cases/XX-9/decisions", json={"action": "keep_monitoring"})
    assert post.status_code == 404 and post.json()["detail"] == "Case not found"


@pytest.mark.parametrize(
    "body",
    [
        {"action": "expel_student"},
        {"action": "factor_looks_wrong"},
        {"action": "factor_looks_wrong", "factor": "weeks_since_active"},
        {"action": "contact_student", "factor": "cum_clicks"},
        {"action": "keep_monitoring", "note": "x" * 1001},
    ],
)
def test_invalid_decisions_are_422(client: TestClient, body: dict) -> None:
    assert client.post("/api/review/cases/OU-1/decisions", json=body).status_code == 422


def test_note_of_exactly_1000_characters_is_stored(client: TestClient) -> None:
    ok = client.post(
        "/api/review/cases/OU-1/decisions", json={"action": "keep_monitoring", "note": "x" * 1000}
    )
    assert ok.status_code == 201 and len(ok.json()["note"]) == 1000


def test_missing_payload_starts_with_no_cases(monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(monkeypatch, with_payload=False) as c:
        assert c.get("/api/review/cases").json() == []
    get_settings.cache_clear()
    reset_engine_for_tests()


def test_decisions_do_not_follow_a_pseudonym_to_another_student(client: TestClient) -> None:
    """A re-export can give OU-1 to a different student; old decisions must not move with it."""
    from src.db.session import get_sessionmaker
    from src.importer.review_payload import import_review_payload

    client.post("/api/review/cases/OU-1/decisions", json={"action": "contact_student"})
    payload = TMP / f"review_{uuid.uuid4().hex}.json"
    write_review_payload(payload, ou1_row=99)
    with get_sessionmaker()() as session:
        import_review_payload(session, payload_path=payload)
    assert client.get("/api/review/cases/OU-1").json()["decisions"] == []
    assert client.get("/api/review/cases").json()[0]["latestDecision"] is None


def test_startup_reimports_a_changed_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    """A re-export must reach a database that already holds the previous cases."""
    run = uuid.uuid4().hex
    with _client(monkeypatch, with_payload=True, run=run) as c:
        assert len(c.get("/api/review/cases").json()) == 2
    path = TMP / f"review_{run}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:1]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with _client(monkeypatch, with_payload=False, run=run) as c:
        assert [x["caseId"] for x in c.get("/api/review/cases").json()] == ["OU-1"]
    get_settings.cache_clear()
    reset_engine_for_tests()
