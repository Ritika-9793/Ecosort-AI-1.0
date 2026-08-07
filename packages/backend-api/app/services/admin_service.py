from datetime import datetime, timezone
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class AdminService:
    """Enterprise Analytics, Audit Logs, and User Management for Super Admins."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_system_analytics(self) -> Dict[str, Any]:
        """Aggregate platform-wide statistics for Admin Dashboard."""
        total_users = await self.db["users"].count_documents({})
        total_scans = await self.db["scans"].count_documents({})
        total_centers = await self.db["recycling_centers"].count_documents({})
        total_pickups = await self.db["doorstep_pickups"].count_documents({})

        # Aggregate total carbon saved
        pipeline = [{"$group": {"_id": None, "total_carbon": {"$sum": "$carbon_saved_kg"}}}]
        carbon_res = await self.db["users"].aggregate(pipeline).to_list(length=1)
        total_carbon = round(carbon_res[0]["total_carbon"], 2) if carbon_res else 0.0

        # Category breakdown
        cat_pipeline = [{"$group": {"_id": "$ai_result.category", "count": {"$sum": 1}}}]
        categories = await self.db["scans"].aggregate(cat_pipeline).to_list(length=10)

        return {
            "total_users": total_users,
            "total_scans": total_scans,
            "total_centers": total_centers,
            "total_pickups": total_pickups,
            "total_carbon_saved_kg": total_carbon,
            "waste_category_breakdown": {c["_id"] or "UNKNOWN": c["count"] for c in categories}
        }

    async def list_users(self, limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        """List platform users with pagination."""
        cursor = self.db["users"].find({}).skip(skip).limit(limit)
        users = []
        async for doc in cursor:
            users.append({
                "id": str(doc["_id"]),
                "full_name": doc.get("full_name"),
                "email": doc.get("email"),
                "role": doc.get("role"),
                "rewards_balance": doc.get("rewards_balance", 0),
                "is_active": doc.get("is_active", True),
                "created_at": doc.get("created_at").isoformat() if isinstance(doc.get("created_at"), datetime) else str(doc.get("created_at"))
            })
        return users

    async def get_audit_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent security audit logs."""
        cursor = self.db["audit_logs"].find({}).sort("timestamp", -1).limit(limit)
        logs = []
        async for doc in cursor:
            logs.append({
                "id": str(doc["_id"]),
                "path": doc.get("path"),
                "method": doc.get("method"),
                "status_code": doc.get("status_code"),
                "client_ip": doc.get("client_ip"),
                "process_time_ms": doc.get("process_time_ms"),
                "timestamp": doc.get("timestamp")
            })
        return logs
