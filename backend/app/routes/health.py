from fastapi import APIRouter

from app.controllers.health import get_health_status

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> dict[str, str]:
    """Expose a lightweight health endpoint for local checks."""
    return dict(get_health_status())
