from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config import settings

def configure_cors(app: FastAPI):
    """
    Configure CORS middleware for the FastAPI application
    """
    # Parse allowed origins from settings
    if settings.CORS_ALLOW_ORIGINS:
        allow_origins = [origin.strip() for origin in settings.CORS_ALLOW_ORIGINS.split(",")]
    else:
        allow_origins = [settings.FRONTEND_URL]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, PATCH, etc.)
        allow_headers=["*"],  # Allow all headers
        expose_headers=["Access-Control-Allow-Origin"],
    )