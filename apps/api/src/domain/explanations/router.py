from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.platform.repository import PlatformRepository

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


@router.get("/global")
def global_explanations(session: DbSession) -> dict:
    return PlatformRepository(session).global_explanations()


@router.get("/cases")
def explanation_cases(session: DbSession) -> list[dict]:
    return PlatformRepository(session).explanation_cases()
