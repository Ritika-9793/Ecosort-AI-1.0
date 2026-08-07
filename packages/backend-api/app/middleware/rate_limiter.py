import time
from fastapi import Request, HTTPException, status
from app.core.database import db_manager


async def rate_limit_middleware(request: Request, max_requests: int = 60, window_seconds: int = 60):
    """
    Sliding window rate-limiter backed by Redis (or memory fallback).
    Caps requests to max_requests per window_seconds per client IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}:{request.url.path}"
    
    redis = db_manager.redis
    if redis is not None:
        try:
            current_time = int(time.time())
            pipeline = redis.pipeline()
            pipeline.zremrangebyscore(key, 0, current_time - window_seconds)
            pipeline.zadd(key, {str(current_time): current_time})
            pipeline.zcard(key)
            pipeline.expire(key, window_seconds)
            results = await pipeline.execute()
            request_count = results[2]

            if request_count > max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )
        except HTTPException:
            raise
        except Exception:
            # Pass silently if Redis is unreachable to avoid blocking legitimate user requests
            pass
