from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdateSchema


class UserService:
    """User Profile Management Engine."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_repo = UserRepository(db)

    async def get_user_profile(self, user_id: str) -> dict:
        """Fetch user profile details by ObjectId."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return {
            "id": str(user["_id"]),
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "role": user.get("role", "CITIZEN"),
            "preferred_language": user.get("preferred_language", "en"),
            "rewards_balance": user.get("rewards_balance", 0),
            "is_active": user.get("is_active", True),
            "created_at": user.get("created_at")
        }

    async def update_user_profile(self, user_id: str, payload: UserUpdateSchema) -> dict:
        """Update profile fields."""
        update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
        if not update_data:
            return await self.get_user_profile(user_id)

        success = await self.user_repo.update(user_id, update_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update profile or no changes submitted"
            )
        return await self.get_user_profile(user_id)
