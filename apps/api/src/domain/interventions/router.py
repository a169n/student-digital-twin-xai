from fastapi import APIRouter

router = APIRouter()


@router.get("")
@router.get("/")
def intervention_scope() -> dict[str, str | list[str]]:
    return {
        "status": "deferred",
        "scope": "research_prototype_placeholder",
        "message": (
            "Intervention workflows are intentionally not implemented in this "
            "foundation. Future work should connect teacher actions to refreshed "
            "predictions and explanations without inventing LMS operations."
        ),
        "futureCapabilities": [
            "record instructor-authored intervention notes",
            "refresh predictions after approved data imports",
            "compare explanation factors before and after a scenario",
        ],
    }
