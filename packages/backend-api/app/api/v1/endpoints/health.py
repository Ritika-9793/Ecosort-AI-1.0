from fastapi import APIRouter
from app.core.config import settings
from app.core.database import db_manager

router = APIRouter()


@router.get("/health", summary="API Health Check Endpoint")
async def health_check():
    """Health check endpoint for Docker & Kubernetes liveness/readiness probes."""
    mongodb_status = "healthy" if db_manager.db is not None else "disconnected"
    redis_status = "healthy" if db_manager.redis is not None else "disconnected"

    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "services": {
            "mongodb": mongodb_status,
            "redis": redis_status
        }
    }
