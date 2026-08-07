from datetime import datetime, timezone
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

BADGES_DEFINITIONS = [
  {"code": "FIRST_SORT", "title": "Eco Pioneer", "description": "Classified your first waste item", "icon": "🌱", "min_scans": 1},
  {"code": "RECYCLER_PRO", "title": "Recycling Champion", "description": "Completed 10 waste classification scans", "icon": "♻️", "min_scans": 10},
  {"code": "CARBON_SAVER", "title": "Carbon Warrior", "description": "Saved 5.0 kg of CO2 emissions", "icon": "🌍", "min_carbon_kg": 5.0},
  {"code": "ECO_LEGEND", "title": "Sustainability Master", "description": "Reached 500 Sustainability Score", "icon": "👑", "min_score": 500}
]

class SustainabilityService:
    """Calculates Sustainability Score, Carbon Offset, and Badges Achievements."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users = db["users"]
        self.scans = db["scans"]

    async def update_user_impact(self, user_id: str, carbon_saved_kg: float, reward_points: int) -> Dict[str, Any]:
        """Update user carbon footprint, eco-coins, sustainability score, and check for new badges."""
        if not ObjectId.is_valid(user_id):
            return {}

        user = await self.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {}

        new_carbon = round(user.get("carbon_saved_kg", 0.0) + carbon_saved_kg, 2)
        new_balance = user.get("rewards_balance", 0) + reward_points
        new_score = user.get("sustainability_score", 0) + int(carbon_saved_kg * 20) + reward_points

        # Calculate scan count
        scan_count = await self.scans.count_documents({"user_id": ObjectId(user_id)})

        # Check badge unlocks
        existing_badges = set(user.get("badges", []))
        newly_unlocked = []

        for b in BADGES_DEFINITIONS:
            if b["code"] not in existing_badges:
                if ("min_scans" in b and scan_count >= b["min_scans"]) or \
                   ("min_carbon_kg" in b and new_carbon >= b["min_carbon_kg"]) or \
                   ("min_score" in b and new_score >= b["min_score"]):
                    existing_badges.add(b["code"])
                    newly_unlocked.append(b)

        # Update MongoDB user record
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "carbon_saved_kg": new_carbon,
                "rewards_balance": new_balance,
                "sustainability_score": new_score,
                "badges": list(existing_badges),
                "updated_at": datetime.now(timezone.utc)
            }}
        )

        return {
            "sustainability_score": new_score,
            "carbon_saved_kg": new_carbon,
            "rewards_balance": new_balance,
            "newly_unlocked_badges": newly_unlocked
        }

    async def get_user_badges(self, user_id: str) -> List[Dict[str, Any]]:
        """Return list of all badges showing unlocked status."""
        user = await self.users.find_one({"_id": ObjectId(user_id)}) if ObjectId.is_valid(user_id) else None
        unlocked_codes = set(user.get("badges", []) if user else [])

        badges_list = []
        for b in BADGES_DEFINITIONS:
            badges_list.append({
                "code": b["code"],
                "title": b["title"],
                "description": b["description"],
                "icon": b["icon"],
                "unlocked": b["code"] in unlocked_codes
            })
        return badges_list

    async def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch top user leaderboard sorted by sustainability score."""
        cursor = self.users.find(
            {"is_active": True},
            {"full_name": 1, "sustainability_score": 1, "carbon_saved_kg": 1, "badges": 1}
        ).sort("sustainability_score", -1).limit(limit)

        leaderboard = []
        rank = 1
        async for doc in cursor:
            leaderboard.append({
                "rank": rank,
                "user_id": str(doc["_id"]),
                "full_name": doc.get("full_name", "Anonymous"),
                "sustainability_score": doc.get("sustainability_score", 0),
                "carbon_saved_kg": doc.get("carbon_saved_kg", 0.0),
                "badges_count": len(doc.get("badges", []))
            })
            rank += 1
        return leaderboard
