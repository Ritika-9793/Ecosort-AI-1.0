from typing import Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserModel


_memory_users: Dict[str, Dict[str, Any]] = {}


class UserRepository:
    """Data Access Object (DAO) for MongoDB users collection."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"email": email.lower()})

    async def get_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"phone": phone})

    async def create(self, user_data: Dict[str, Any]) -> str:
        user_data["email"] = user_data["email"].lower()
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)

    async def update(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def update_rewards(self, user_id: str, points_increment: int) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"rewards_balance": points_increment}}
        )
        return result.modified_count > 0


class InMemoryUserRepository:
    """Development-only user store used when MongoDB is unavailable."""

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        normalized_email = email.lower()
        return next(
            (user for user in _memory_users.values() if user["email"] == normalized_email),
            None,
        )

    async def get_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        return next(
            (user for user in _memory_users.values() if user.get("phone") == phone),
            None,
        )

    async def create(self, user_data: Dict[str, Any]) -> str:
        user_id = str(ObjectId())
        user_data["_id"] = user_id
        _memory_users[user_id] = user_data
        return user_id
