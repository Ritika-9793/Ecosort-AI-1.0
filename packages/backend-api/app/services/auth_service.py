from datetime import datetime, timezone
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegisterSchema, UserLoginSchema
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.config import settings


class AuthService:
    """Authentication and Authorization Business Engine."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_repo = UserRepository(db)

    async def register_user(self, payload: UserRegisterSchema) -> dict:
        """Register a new user in the platform."""
        # Check existing email
        existing_email = await self.user_repo.get_by_email(payload.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )

        # Check existing phone if provided
        if payload.phone:
            existing_phone = await self.user_repo.get_by_phone(payload.phone)
            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this phone number already exists."
                )

        hashed_pwd = get_password_hash(payload.password)
        user_dict = {
            "full_name": payload.full_name,
            "email": payload.email.lower(),
            "phone": payload.phone,
            "hashed_password": hashed_pwd,
            "role": payload.role.upper(),
            "preferred_language": payload.preferred_language,
            "rewards_balance": 0,
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        user_id = await self.user_repo.create(user_dict)
        return {
            "id": user_id,
            "email": payload.email,
            "full_name": payload.full_name,
            "role": payload.role.upper()
        }

    async def authenticate_user(self, payload: UserLoginSchema) -> dict:
        """Authenticate user credentials and generate OAuth2 JWT tokens."""
        user = await self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated. Contact support."
            )

        user_id = str(user["_id"])
        role = user.get("role", "CITIZEN")

        access_token = create_access_token(subject=user_id, role=role)
        refresh_token = create_refresh_token(subject=user_id, role=role)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user_id,
                "full_name": user["full_name"],
                "email": user["email"],
                "role": role,
                "preferred_language": user.get("preferred_language", "en"),
                "rewards_balance": user.get("rewards_balance", 0),
                "is_active": user.get("is_active", True),
                "created_at": user.get("created_at").isoformat() if isinstance(user.get("created_at"), datetime) else str(user.get("created_at"))
            }
        }
