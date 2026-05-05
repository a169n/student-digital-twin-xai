from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.platform.repository import PlatformRepository

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


@router.get("")
@router.get("/")
def list_students(session: DbSession) -> list[dict]:
    return PlatformRepository(session).list_students()


@router.get("/{student_id}")
def get_student(student_id: str, session: DbSession) -> dict:
    detail = PlatformRepository(session).get_student_detail(student_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return detail
