from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from fastapi import Depends
from .engine import AsyncSessionLocal

# Dependency for getting database session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session for FastAPI endpoints
    """
    async with AsyncSessionLocal() as session:
        yield session