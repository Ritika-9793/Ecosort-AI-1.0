from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.common import ResponseSchema
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/analytics", response_model=ResponseSchema[dict])
async def get_admin_analytics(
    auth: dict = Depends(require_roles(["ADMIN"])),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Super Admin Analytics Endpoint."""
    service = AdminService(db)
    analytics = await service.get_system_analytics()
    return ResponseSchema(success=True, data=analytics)


@router.get("/users", response_model=ResponseSchema[dict])
async def get_admin_users(
    limit: int = 50,
    skip: int = 0,
    auth: dict = Depends(require_roles(["ADMIN"])),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """List platform users with pagination."""
    service = AdminService(db)
    users = await service.list_users(limit, skip)
    return ResponseSchema(success=True, data={"users": users})


@router.get("/audit-logs", response_model=ResponseSchema[dict])
async def get_audit_logs(
    limit: int = 50,
    auth: dict = Depends(require_roles(["ADMIN"])),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve security audit logs."""
    service = AdminService(db)
    logs = await service.get_audit_logs(limit)
    return ResponseSchema(success=True, data={"audit_logs": logs})
