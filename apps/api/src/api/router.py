from fastapi import APIRouter

from src.api.routes import health
from src.domain.explanations.router import router as explanations_router
from src.domain.interventions.router import router as interventions_router
from src.domain.predictions.router import router as predictions_router
from src.domain.students.router import router as students_router
from src.domain.twins.router import router as twins_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(students_router, prefix="/students", tags=["students"])
api_router.include_router(twins_router, prefix="/twins", tags=["twins"])
api_router.include_router(predictions_router, prefix="/predictions", tags=["predictions"])
api_router.include_router(interventions_router, prefix="/interventions", tags=["interventions"])
api_router.include_router(explanations_router, prefix="/explanations", tags=["explanations"])
