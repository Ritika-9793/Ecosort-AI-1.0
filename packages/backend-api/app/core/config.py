from pathlib import Path
from typing import List, Union, Any
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    """Application Core Settings loaded from Environment Variables."""
    
    APP_NAME: str = "EcoSort AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Auth Security Secrets
    SECRET_KEY: str = "super_secret_jwt_key_ecosort_ai_sprint_1_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # MongoDB Database Connection
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "ecosort_db"
    
    # Redis Caching
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS Origins
    CORS_ORIGINS: Any = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return ["*"]
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
            try:
                import json
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else [str(parsed)]
            except Exception:
                return [v]
        elif isinstance(v, list):
            return [str(item) for item in v]
        return ["*"]

    # Security & Upload Validation
    MAX_UPLOAD_SIZE_BYTES: int = 5_242_880  # 5 MB
    ALLOWED_MIME_TYPES: Any = ["image/jpeg", "image/png", "image/webp"]

    @field_validator("ALLOWED_MIME_TYPES", mode="before")
    def parse_mime_types(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return ["image/jpeg", "image/png", "image/webp"]
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
            try:
                import json
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else [str(parsed)]
            except Exception:
                return [v]
        elif isinstance(v, list):
            return [str(item) for item in v]
        return ["image/jpeg", "image/png", "image/webp"]

    # AI Engine Model Settings
    AI_MODEL_PATH: str = "packages/ai-engine/saved_models/mobilenetv3_waste_v1.tflite"
    MIN_CONFIDENCE_THRESHOLD: float = 0.70

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
