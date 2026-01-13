from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import settings

SECRET_KEY = settings.BETTER_AUTH_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours

def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT token, returning the payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            return None

        return payload
    except JWTError:
        # Invalid token
        return None

def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token payload
    """
    payload = decode_jwt_token(token)
    if payload:
        # Better Auth typically stores user ID in the "sub" (subject) claim
        user_id = payload.get("sub")
        if user_id:
            return str(user_id)
    return None

def verify_token_and_get_user_id(token: str) -> Optional[str]:
    """
    Verify JWT token and return user_id if valid
    """
    return extract_user_id_from_token(token)