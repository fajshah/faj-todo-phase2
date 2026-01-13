from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from exceptions import (
    TaskNotFoundError, TaskOwnershipError, ValidationError,
    DatabaseError, ServiceError
)
from schemas.task import ErrorResponse

async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    """
    Handler for TaskNotFoundError
    """
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(detail=str(exc.detail)).dict()
    )

async def task_ownership_error_handler(request: Request, exc: TaskOwnershipError):
    """
    Handler for TaskOwnershipError
    """
    return JSONResponse(
        status_code=403,
        content=ErrorResponse(detail=str(exc.detail)).dict()
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    """
    Handler for ValidationError
    """
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(detail=str(exc.detail)).dict()
    )

async def database_error_handler(request: Request, exc: DatabaseError):
    """
    Handler for DatabaseError
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(detail=str(exc.detail)).dict()
    )

async def service_error_handler(request: Request, exc: ServiceError):
    """
    Handler for ServiceError
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=str(exc.detail)).dict()
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.detail).dict()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for request validation errors
    """
    errors = []
    for error in exc.errors():
        errors.append(f"{error['loc'][-1]}: {error['msg']}")

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(detail="; ".join(errors)).dict()
    )

# Dictionary of handlers to register with FastAPI app
exception_handlers = {
    TaskNotFoundError: task_not_found_handler,
    TaskOwnershipError: task_ownership_error_handler,
    ValidationError: validation_error_handler,
    DatabaseError: database_error_handler,
    ServiceError: service_error_handler,
    StarletteHTTPException: http_exception_handler,
    RequestValidationError: validation_exception_handler,
}