from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.platform.repository import PlatformRepository

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


@router.get("/{student_id}/snapshots")
def get_student_snapshots(student_id: str, session: DbSession) -> list[dict]:
    snapshots = PlatformRepository(session).get_snapshots(student_id)
    if snapshots is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return snapshots
