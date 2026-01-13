from fastapi import HTTPException, status

class TaskNotFoundError(HTTPException):
    """
    Exception raised when a task is not found
    """
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

class TaskOwnershipError(HTTPException):
    """
    Exception raised when a user tries to access another user's task
    """
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied - task {task_id} does not belong to user"
        )

class ValidationError(HTTPException):
    """
    Exception raised for validation errors
    """
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class DatabaseError(HTTPException):
    """
    Exception raised for database errors
    """
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ServiceError(HTTPException):
    """
    General exception for service-level errors
    """
    def __init__(self, detail: str = "Service error occurred", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            status_code=status_code,
            detail=detail
        )