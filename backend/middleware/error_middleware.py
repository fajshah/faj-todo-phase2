from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from errors.handlers import exception_handlers
import traceback
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle errors globally
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Log the error
            logger.error(f"Unhandled error: {str(exc)}")
            logger.error(traceback.format_exc())

            # Check if there's a specific handler for this exception type
            handler = exception_handlers.get(type(exc))
            if handler:
                # Use the specific handler
                return await handler(request, exc)

            # Default error response for unhandled exceptions
            from schemas.task import ErrorResponse
            return JSONResponse(
                status_code=500,
                content=ErrorResponse(
                    detail="Internal server error",
                    success=False
                ).dict()
            )