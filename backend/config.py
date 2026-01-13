from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
class Settings(BaseSettings):
    NEON_DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ALLOW_ORIGINS: Optional[str] = None  # Comma-separated list of origins
    MONGODB_URI: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    JWT_EXPIRE: Optional[str] = None
    PORT: Optional[int] = 5000

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  

# Create settings instance
settings = Settings()

def validate_environment():
    """
    Validate that required environment variables are set
    """
    errors = []

    if not settings.NEON_DATABASE_URL:
        errors.append("NEON_DATABASE_URL environment variable is required")

    if not settings.BETTER_AUTH_SECRET:
        errors.append("BETTER_AUTH_SECRET environment variable is required")

    if errors:
        raise ValueError(f"Missing required environment variables: {'; '.join(errors)}")

# Validate settings on import
validate_environment()