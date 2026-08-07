from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger


async def global_exception_handler(request: Request, exc: Exception):
    """Global exception middleware catching unhandled runtime exceptions."""
    logger.error(
        "Unhandled System Error",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "details": "An internal server error occurred. Please contact system administrator."
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format Pydantic validation errors into standard response format."""
    logger.warning("Request Validation Failed", path=request.url.path, errors=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "details": exc.errors()
            }
        }
    )
