from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database import db_manager
from app.core.logging import logger


class AuditLoggerMiddleware(BaseHTTPMiddleware):
    """Middleware capturing security and API access audit logs into MongoDB asynchronously."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now(timezone.utc)
        response = await call_next(request)
        process_time_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0

        # Log sensitive endpoints asynchronously
        if request.url.path.startswith("/api/v1"):
            client_ip = request.client.host if request.client else "127.0.0.1"
            audit_entry = {
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "client_ip": client_ip,
                "process_time_ms": round(process_time_ms, 2),
                "timestamp": start_time.isoformat()
            }
            
            logger.info("API Audit Event", **audit_entry)

            # Store in MongoDB audit_logs if DB connection is active
            if db_manager.db is not None:
                try:
                    await db_manager.db["audit_logs"].insert_one(audit_entry)
                except Exception as e:
                    logger.warning("Failed to record audit log to MongoDB", error=str(e))

        return response
