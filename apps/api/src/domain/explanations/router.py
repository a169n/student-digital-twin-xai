from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_placeholder() -> dict[str, str]:
    return {"status": "placeholder"}
