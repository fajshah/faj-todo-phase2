from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from typing import AsyncGenerator
from sqlmodel import SQLModel
import asyncio

# Create async engine for database (using SQLite for development)
# In production, this would use the Neon PostgreSQL URL
database_url = settings.NEON_DATABASE_URL

# For development, if using SQLite, we need to handle the async driver
if database_url.startswith("sqlite"):
    # Use SQLite with aiosqlite-compatible async adapter
    async_database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///") if not database_url.startswith("sqlite+aiosqlite") else database_url
else:
    # For PostgreSQL, use asyncpg
    async_database_url = database_url if "+asyncpg" in database_url else database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
if database_url.startswith("sqlite"):
    # SQLite doesn't support connection pooling parameters
    async_engine = create_async_engine(
        async_database_url,
        echo=True,  # Set to False in production
    )

    # Create sync engine as backup (for sync operations)
    sync_database_url = database_url.replace('+aiosqlite', '').replace('sqlite+aiosqlite:///', 'sqlite:///')
    sync_engine = create_engine(
        sync_database_url,
        echo=True,  # Set to False in production
    )
else:
    # For PostgreSQL, use connection pooling parameters
    async_engine = create_async_engine(
        async_database_url,
        echo=True,  # Set to False in production
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
    )

    # Create sync engine as backup (for sync operations)
    sync_database_url = database_url.replace('+asyncpg', '').replace('postgresql+asyncpg://', 'postgresql://')
    sync_engine = create_engine(
        sync_database_url,
        echo=True,  # Set to False in production
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)

# Create sync session maker
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

# Export engines for use in main.py
engine = sync_engine

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session
    """
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_session():
    """
    Get sync database session
    """
    with SyncSessionLocal() as session:
        yield session

async def create_db_and_tables():
    """
    Create database tables
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)