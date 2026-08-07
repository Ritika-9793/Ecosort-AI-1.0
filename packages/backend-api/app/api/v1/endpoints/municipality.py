from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.core.security import require_roles
from app.schemas.common import ResponseSchema
from app.services.municipality_service import MunicipalityService

router = APIRouter()


@router.get("/ward-stats", response_model=ResponseSchema[dict])
async def get_municipal_ward_stats(
    auth: dict = Depends(require_roles(["MUNICIPALITY", "ADMIN"])),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve municipal ward-wise waste generation statistics."""
    service = MunicipalityService(db)
    ward_stats = await service.get_ward_distribution()
    return ResponseSchema(success=True, data={"ward_stats": ward_stats})


@router.get("/heatmap", response_model=ResponseSchema[dict])
async def get_municipal_heatmap(
    auth: dict = Depends(require_roles(["MUNICIPALITY", "ADMIN"])),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retrieve GIS spatial scan clusters for illegal dumping heatmaps."""
    service = MunicipalityService(db)
    points = await service.get_heatmap_coordinates()
    return ResponseSchema(success=True, data={"total_points": len(points), "points": points})
