from datetime import datetime, timezone
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.core.logging import logger

class NotificationService:
    """In-App and FCM Push Notification Service Engine."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.notifications = db["notifications"]

    async def create_notification(self, user_id: str, title: str, message: str, notification_type: str = "INFO") -> str:
        """Create an in-app notification entry for a user."""
        doc = {
            "user_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False,
            "created_at": datetime.now(timezone.utc)
        }
        res = await self.notifications.insert_one(doc)
        logger.info("Notification created", user_id=user_id, title=title)
        return str(res.inserted_id)

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch user notifications."""
        if not ObjectId.is_valid(user_id):
            return []
        cursor = self.notifications.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit)
        items = []
        async for doc in cursor:
            items.append({
                "id": str(doc["_id"]),
                "title": doc.get("title"),
                "message": doc.get("message"),
                "type": doc.get("type", "INFO"),
                "is_read": doc.get("is_read", False),
                "created_at": doc.get("created_at").isoformat() if isinstance(doc.get("created_at"), datetime) else str(doc.get("created_at"))
            })
        return items

    async def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """Mark notification as read."""
        if not ObjectId.is_valid(notification_id) or not ObjectId.is_valid(user_id):
            return False
        res = await self.notifications.update_one(
            {"_id": ObjectId(notification_id), "user_id": ObjectId(user_id)},
            {"$set": {"is_read": True}}
        )
        return res.modified_count > 0
