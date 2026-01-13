from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    """
    Enum for task status filtering
    """
    pending = "pending"
    completed = "completed"
    all = "all"

class TaskBase(BaseModel):
    """
    Base schema for Task with common fields
    """
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """
    Schema for creating new tasks
    """
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    """
    Schema for updating tasks
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """
    Schema for task responses
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskListResponse(BaseModel):
    """
    Schema for task list responses
    """
    data: List[TaskResponse]
    success: bool = True

class TaskSingleResponse(BaseModel):
    """
    Schema for single task responses
    """
    data: TaskResponse
    success: bool = True

class SuccessResponse(BaseModel):
    """
    Schema for success responses
    """
    success: bool = True

class ErrorResponse(BaseModel):
    """
    Schema for error responses
    """
    detail: str
    success: bool = False