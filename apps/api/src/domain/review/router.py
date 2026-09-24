from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db_session
from src.domain.review.models import DecisionIn
from src.domain.review.repository import ReviewRepository
from src.domain.review.service import CaseNotFound, FactorNotShown, ReviewService

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db_session)]


def _service(session: Session) -> ReviewService:
    return ReviewService(ReviewRepository(session))


@router.get("/cases")
def list_cases(session: DbSession) -> list[dict]:
    return _service(session).list_cases()


@router.get("/cases/{case_id}")
def get_case(case_id: str, session: DbSession) -> dict:
    try:
        return _service(session).get_case(case_id)
    except CaseNotFound:
        raise HTTPException(status_code=404, detail="Case not found") from None


@router.post("/cases/{case_id}/decisions", status_code=201)
def record_decision(case_id: str, decision: DecisionIn, session: DbSession) -> dict:
    try:
        return _service(session).record_decision(case_id, decision)
    except CaseNotFound:
        raise HTTPException(status_code=404, detail="Case not found") from None
    except FactorNotShown:
        raise HTTPException(
            status_code=422, detail="factor must be one of the case's shown factors"
        ) from None
