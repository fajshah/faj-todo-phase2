"""
Production-ready configuration for the Phase II Todo Backend API
"""

import os
from enum import Enum
from typing import Optional

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

def get_environment() -> Environment:
    """Get the current environment from the ENVIRONMENT environment variable."""
    env_str = os.getenv("ENVIRONMENT", "development").lower()
    try:
        return Environment(env_str)
    except ValueError:
        return Environment.DEVELOPMENT

def is_production() -> bool:
    """Check if the current environment is production."""
    return get_environment() == Environment.PRODUCTION

def is_development() -> bool:
    """Check if the current environment is development."""
    return get_environment() == Environment.DEVELOPMENT

def is_testing() -> bool:
    """Check if the current environment is testing."""
    return get_environment() == Environment.TESTING

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if is_production() else "DEBUG")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Database configuration
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # 1 hour

# API configuration
API_V1_STR = "/api/v1"
PROJECT_NAME = "Phase II Todo Backend API"

# Security configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# JWT configuration
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Performance configuration
MAX_TASKS_PER_USER = int(os.getenv("MAX_TASKS_PER_USER", "1000"))
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = int(os.getenv("MAX_DESCRIPTION_LENGTH", "10000"))

# Feature flags
ENABLE_TASK_SHARING = os.getenv("ENABLE_TASK_SHARING", "false").lower() == "true"
ENABLE_TASK_ATTACHMENTS = os.getenv("ENABLE_TASK_ATTACHMENTS", "false").lower() == "true"