from typing import Optional
from errors.exceptions import ValidationError

def validate_task_title(title: Optional[str]) -> None:
    """
    Validate task title length (1-200 characters)
    """
    if title is None:
        raise ValidationError("Task title is required")

    if len(title) < 1:
        raise ValidationError("Task title must be at least 1 character")

    if len(title) > 200:
        raise ValidationError("Task title must be no more than 200 characters")

def validate_task_description(description: Optional[str]) -> None:
    """
    Validate task description (currently just checks if it's too long)
    """
    if description and len(description) > 10000:  # Arbitrary limit for description
        raise ValidationError("Task description is too long")

def validate_task_completion(completion_status: Optional[bool]) -> None:
    """
    Validate task completion status is a boolean value
    """
    if completion_status is not None and not isinstance(completion_status, bool):
        raise ValidationError("Task completion status must be a boolean value")

def validate_task_data(
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> None:
    """
    Validate task data for creation or updates
    """
    if title is not None:
        validate_task_title(title)

    if description is not None:
        validate_task_description(description)

    if completed is not None:
        validate_task_completion(completed)