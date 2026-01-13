from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import verify_token_and_get_user_id

security = HTTPBearer()

async def get_current_user_id(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    FastAPI dependency to get the current user's ID from JWT token
    """
    token = credentials.credentials

    user_id = verify_token_and_get_user_id(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

# Alternative dependency that returns the raw token if needed
async def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    FastAPI dependency to get the current JWT token
    """
    return credentials.credentials