from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import get_settings
from src.domain.platform.bootstrap import initialize_platform_store

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_platform_store()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(api_router)
