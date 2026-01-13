from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    """
    Exception raised for authentication errors
    """
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthorizationError(HTTPException):
    """
    Exception raised for authorization errors (access denied)
    """
    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class TokenValidationError(HTTPException):
    """
    Exception raised for token validation errors
    """
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ExpiredTokenError(TokenValidationError):
    """
    Exception raised for expired tokens
    """
    def __init__(self):
        super().__init__("Token has expired")