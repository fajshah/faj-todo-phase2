from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from models.user import User, UserCreate
from auth.hashing import hash_password, verify_password
from datetime import datetime
import uuid

class AuthService:
    @staticmethod
    async def create_user(user_data: UserCreate, db_session: AsyncSession) -> User:
        # Check if user already exists
        result = await db_session.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create new user
        user = User(
            id=uuid.uuid4(),
            email=user_data.email,
            password_hash=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to database
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        return user

    @staticmethod
    async def authenticate_user(email: str, password: str, db_session: AsyncSession) -> Optional[User]:
        # Find user by email
        result = await db_session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            return None

        return user