from __future__ import annotations

from pathlib import Path

from src.core.config import get_settings
from src.db import init_db
from src.db.session import get_sessionmaker
from src.importer.research_payload import import_research_payload


def main() -> None:
    settings = get_settings()
    payload_path = Path(settings.research_demo_payload_path)
    init_db()
    with get_sessionmaker()() as session:
        summary = import_research_payload(session, payload_path=payload_path)
    print(
        "Imported research platform seed: "
        f"{summary.student_count} students, "
        f"{summary.snapshot_count} weekly snapshots, "
        f"{summary.explanation_case_count} explanation cases"
    )


if __name__ == "__main__":
    main()
