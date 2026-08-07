from typing import Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserModel


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
