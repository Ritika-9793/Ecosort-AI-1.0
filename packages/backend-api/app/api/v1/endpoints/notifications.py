from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user_id
from app.schemas.common import ResponseSchema
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("", response_model=ResponseSchema[dict])
async def get_notifications(
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve user in-app notifications."""
    service = NotificationService(db)
    notifications = await service.get_user_notifications(user_id)
    return ResponseSchema(success=True, data={"notifications": notifications})


@router.patch("/{notification_id}/read", response_model=ResponseSchema[dict])
async def mark_notification_read(
    notification_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Mark a notification as read."""
    service = NotificationService(db)
    success = await service.mark_as_read(notification_id, user_id)
    return ResponseSchema(success=success, message="Notification marked as read")
