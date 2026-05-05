from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.platform.repository import PlatformRepository

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


@router.get("/latest")
def latest_predictions(session: DbSession) -> dict:
    return PlatformRepository(session).latest_predictions()
