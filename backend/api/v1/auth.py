from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict
from models.user import UserCreate, UserRead
from database.session import get_async_session
from services.auth_service import AuthService
from auth.utils import create_access_token
from datetime import timedelta
import uuid

router = APIRouter(tags=["auth"])

@router.post("/auth/signup", response_model=UserRead)
async def signup(user_create: UserCreate, db_session: AsyncSession = Depends(get_async_session)):
    try:
        # Create user using auth service
        user = await AuthService.create_user(user_create, db_session)

        # Create access token
        access_token_expires = timedelta(minutes=30)  # Temporary token for signup
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        # Return user info with token
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/auth/login")
async def login(email: str, password: str, db_session: AsyncSession = Depends(get_async_session)):
    user = await AuthService.authenticate_user(email, password, db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/logout")
async def logout():
    # In a real implementation, you might want to blacklist the token
    # For now, just return a success message
    return {"message": "Successfully logged out"}