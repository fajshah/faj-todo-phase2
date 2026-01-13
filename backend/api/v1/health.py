from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from database.session import get_async_session
from models.user import User
from sqlmodel import select

router = APIRouter(tags=["health"])

@router.get("/health", summary="Health Check")
async def health_check():
    """
    Basic health check endpoint to verify backend is running
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/health/database", summary="Database Health Check")
async def database_health_check():
    """
    Health check endpoint to verify database connectivity
    """
    try:
        # Get a database session to test connectivity
        async with get_async_session() as session:
            # Try a simple query to verify database is accessible
            statement = select(User).limit(1)
            await session.exec(statement)

        return {
            "status": "database_healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")