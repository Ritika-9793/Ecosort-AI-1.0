from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user_id
from app.schemas.common import ResponseSchema
from app.services.sustainability_service import SustainabilityService

router = APIRouter()


@router.get("/badges", response_model=ResponseSchema[dict])
async def get_user_badges(
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve badges and achievements unlocked status."""
    service = SustainabilityService(db)
    badges = await service.get_user_badges(user_id)
    return ResponseSchema(success=True, data={"badges": badges})


@router.get("/leaderboard", response_model=ResponseSchema[dict])
async def get_sustainability_leaderboard(
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve global user sustainability leaderboard."""
    service = SustainabilityService(db)
    leaderboard = await service.get_leaderboard(limit)
    return ResponseSchema(success=True, data={"leaderboard": leaderboard})
