import sys
from pathlib import Path

# Ensure project root (containing 'packages') is in sys.path
_curr = Path(__file__).resolve()
while _curr.parent != _curr:
    if (_curr / "packages").exists() or (_curr / ".git").exists():
        if str(_curr) not in sys.path:
            sys.path.insert(0, str(_curr))
        break
    _curr = _curr.parent

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.database import connect_to_databases, close_database_connections
from app.middleware.error_handler import global_exception_handler, validation_exception_handler
from app.middleware.audit_logger import AuditLoggerMiddleware
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Context Manager handling startup and shutdown initialization."""
    setup_logging()
    logger.info("Initializing EcoSort AI Backend Engine...", app_name=settings.APP_NAME, env=settings.APP_ENV)
    
    # Establish Async MongoDB & Redis Connections
    await connect_to_databases()
    
    yield
    
    # Clean shutdown
    logger.info("Shutting down EcoSort AI Backend Engine...")
    await close_database_connections()


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Setup CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in settings.CORS_ORIGINS else settings.CORS_ORIGINS,
    allow_origin_regex=(
        r"^https?://(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+)(:\d+)?$"
        if settings.APP_ENV == "development"
        else None
    ),
    allow_credentials=False if "*" in settings.CORS_ORIGINS else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Security Audit Logger Middleware
app.add_middleware(AuditLoggerMiddleware)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Register Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "title": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
