import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.core.logging import logger


class DatabaseManager:
    """Singleton Async Database Connection Manager for MongoDB and Redis."""
    
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None
    redis: aioredis.Redis = None


db_manager = DatabaseManager()


async def connect_to_databases():
    """Establish async connection to MongoDB Atlas and Redis."""
    try:
        logger.info("Connecting to MongoDB...")
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )
        db_manager.db = db_manager.client[settings.MONGODB_DATABASE]
        
        # Ping database
        await db_manager.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB", database=settings.MONGODB_DATABASE)

        # Initialize Collections and Indexes
        await setup_database_indexes()
        await seed_initial_knowledge_base()

    except Exception as e:
        if db_manager.client:
            db_manager.client.close()
        db_manager.client = None
        db_manager.db = None
        logger.error("MongoDB connection failed", error=str(e))
        if settings.APP_ENV.lower() == "production":
            raise RuntimeError(
                "MongoDB is required in production. Set MONGODB_URI to a reachable MongoDB deployment."
            ) from e
        logger.warning("MongoDB unavailable; development auth fallback is enabled.")

    try:
        logger.info("Connecting to Redis Cache...", redis_url=settings.REDIS_URL)
        db_manager.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await db_manager.redis.ping()
        logger.info("Successfully connected to Redis Cache")
    except Exception as e:
        if db_manager.redis:
            await db_manager.redis.close()
        db_manager.redis = None
        logger.warning("Redis connection unavailable, proceeding with in-memory fallback", error=str(e))


async def close_database_connections():
    """Gracefully close database clients on server shutdown."""
    if db_manager.client:
        logger.info("Closing MongoDB connection...")
        db_manager.client.close()
    if db_manager.redis:
        logger.info("Closing Redis connection...")
        await db_manager.redis.close()


async def setup_database_indexes():
    """Ensure database collections and spatial 2dsphere indexes exist."""
    db = db_manager.db
    
    # User indexes
    await db["users"].create_index("email", unique=True)
    await db["users"].create_index("phone", unique=True, sparse=True)
    
    # Recycling centers spatial 2dsphere index
    await db["recycling_centers"].create_index([("location", "2dsphere")])
    
    # Waste knowledge base index
    await db["waste_knowledge_base"].create_index("category_code", unique=True)
    
    # Scans indexes
    await db["scans"].create_index([("user_id", 1), ("created_at", -1)])
    await db["scans"].create_index("perceptual_hash")
    
    # Audit log index
    await db["audit_logs"].create_index([("timestamp", -1)])

    logger.info("MongoDB collection indexes initialized successfully.")


async def seed_initial_knowledge_base():
    """Seed baseline Indian MSW disposal rules into waste_knowledge_base collection."""
    db = db_manager.db
    kb_collection = db["waste_knowledge_base"]
    
    count = await kb_collection.count_documents({})
    if count == 0:
        logger.info("Seeding waste_knowledge_base collection with initial rules...")
        seed_data = [
            {
                "category_code": "PLASTIC_PET_BOTTLE",
                "display_name_en": "PET Plastic Bottle",
                "display_name_hi": "पीईटी प्लास्टिक की बोतल",
                "waste_type": "DRY_RECYCLABLE",
                "bin_color": "BLUE",
                "urban_instructions_en": "Rinse, crush bottle, unscrew cap, dispose in Blue Dry Waste bin.",
                "urban_instructions_hi": "धोएं, बोतल को कुचलें, ढक्कन खोलें, नीले सूखे कचरे के डिब्बे में डालें।",
                "rural_instructions_en": "Store clean bottles in dry sack; sell to local Kabadiwala during weekly visit.",
                "rural_instructions_hi": "साफ बोतलों को सूखी बोरी में रखें; साप्ताहिक यात्रा के दौरान स्थानीय कबाड़ीवाले को बेचें।",
                "eco_coins_reward": 10,
                "is_active": True
            },
            {
                "category_code": "ORGANIC_KITCHEN_WASTE",
                "display_name_en": "Kitchen Waste & Food Scraps",
                "display_name_hi": "रसोई का गीला कचरा",
                "waste_type": "WET_ORGANIC",
                "bin_color": "GREEN",
                "urban_instructions_en": "Dispose directly into Green Wet Waste Bin for municipal composting.",
                "urban_instructions_hi": "नगर निगम की खाद के लिए सीधे हरे गीले कचरे के डिब्बे में डालें।",
                "rural_instructions_en": "Add to household compost pit or feed to livestock.",
                "rural_instructions_hi": "घरेलू कंपोस्ट गड्ढे में डालें या मवेशियों को खिलाएं।",
                "eco_coins_reward": 5,
                "is_active": True
            },
            {
                "category_code": "E_WASTE_BATTERY",
                "display_name_en": "Used Battery & Electronics",
                "display_name_hi": "इलेक्ट्रॉनिक व प्रयुक्त बैटरी",
                "waste_type": "HAZARDOUS",
                "bin_color": "BLACK",
                "urban_instructions_en": "Drop off at designated E-Waste collection kiosk or municipal hazardous center.",
                "urban_instructions_hi": "ई-कचरा संग्रह कियोस्क या नगर निगम खतरनाक केंद्र पर जमा करें।",
                "rural_instructions_en": "Keep isolated in a sealed container away from water source; hand over to hazardous e-waste collection drive.",
                "rural_instructions_hi": "पानी के स्रोत से दूर एक सील कंटेनर में रखें; ई-कचरा संग्रह अभियान को सौंपें।",
                "eco_coins_reward": 25,
                "is_active": True
            }
        ]
        await kb_collection.insert_many(seed_data)
        logger.info("Knowledge base successfully seeded.")


def get_db() -> AsyncIOMotorDatabase:
    """Dependency injection helper to get MongoDB database instance."""
    if db_manager.db is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is unavailable. Ensure MongoDB service is running."
        )
    return db_manager.db


def get_optional_db() -> AsyncIOMotorDatabase:
    """Return the database when available so development fallbacks can be used."""
    return db_manager.db
