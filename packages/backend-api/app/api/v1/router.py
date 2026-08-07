from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    users,
    waste,
    centers,
    pickups,
    rewards,
    notifications,
    admin,
    municipality
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health Probe"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["User Profiles"])
api_router.include_router(waste.router, prefix="/waste", tags=["AI Waste Classification"])
api_router.include_router(centers.router, prefix="/centers", tags=["Recycling Locator"])
api_router.include_router(pickups.router, prefix="/pickups", tags=["Doorstep Scrap Pickups"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["Gamification & Badges"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notification Center"])
api_router.include_router(admin.router, prefix="/admin", tags=["Super Admin Analytics"])
api_router.include_router(municipality.router, prefix="/municipality", tags=["Municipal Ward Analytics"])
