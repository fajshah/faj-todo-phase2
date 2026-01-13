from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.requests import Request
from api.v1.tasks import router as tasks_router
from api.v1.auth import router as auth_router
from api.v1.health import router as health_router
from middleware.cors import configure_cors
from contextlib import asynccontextmanager
from database.engine import create_db_and_tables
import logging

# Define exception handlers
exception_handlers = {}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events
    """
    logger.info("Starting up...")
    # Create database tables
    await create_db_and_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down...")

# Create FastAPI app instance
app = FastAPI(
    title="Phase II Todo Backend API",
    description="Backend API for the Phase II Todo Full-Stack Web Application",
    version="1.0.0",
    lifespan=lifespan
)

# Register exception handlers
for exc_type, handler in exception_handlers.items():
    app.add_exception_handler(exc_type, handler)

# Configure CORS
configure_cors(app)

# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(health_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phase II Todo Backend API"}

# Add exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"],
                }
                for error in exc.errors()
            ]
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)