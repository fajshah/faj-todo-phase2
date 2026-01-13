from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    """
    Base model for Task with common fields
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=None)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Indexed for efficient user-based queries

class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskPublic(TaskBase):
    """
    Public representation of Task (without internal fields)
    """
    id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    """
    Model for updating task fields
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskCreate(TaskBase):
    """
    Model for creating new tasks
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    user_id: str