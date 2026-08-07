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
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
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
