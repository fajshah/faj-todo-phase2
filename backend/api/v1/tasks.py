from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from database.session import get_async_session
from auth.dependencies import get_current_user_id
from schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskSingleResponse, SuccessResponse, ErrorResponse, TaskStatus
)
from models.task import Task as TaskModel
from controllers.task_controller import TaskController
from validators.task_validator import validate_task_data
from errors.exceptions import TaskNotFoundError, TaskOwnershipError, ValidationError

router = APIRouter(tags=["tasks"])

@router.post("/", response_model=TaskSingleResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user
    """
    # Validate task data
    validate_task_data(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    # Prepare task data with user_id
    task_with_user = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    try:
        # Create task in database
        created_task = await TaskController.create_task(session, task_with_user)

        # Create response object manually
        task_response = TaskResponse(
            id=created_task.id,
            title=created_task.title,
            description=created_task.description,
            completed=created_task.completed,
            user_id=created_task.user_id,
            created_at=created_task.created_at,
            updated_at=created_task.updated_at
        )
        return TaskSingleResponse(data=task_response)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Error creating task"
        )


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    status_param: Optional[TaskStatus] = Query(None, description="Filter tasks by status (pending/completed/all)"),
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for the authenticated user with optional filtering
    """
    tasks = await TaskController.get_tasks(session, user_id, status_param)

    # Convert to response format
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        task_responses.append(task_response)

    return TaskListResponse(data=task_responses)


@router.get("/{task_id}", response_model=TaskSingleResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task for the authenticated user
    """
    task = await TaskController.get_task_by_id(session, task_id, user_id)

    if not task:
        raise TaskNotFoundError(task_id)

    task_response = TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

    return TaskSingleResponse(data=task_response)


@router.put("/{task_id}", response_model=TaskSingleResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for the authenticated user
    """
    # Validate update data
    validate_task_data(
        title=task_update.title,
        description=task_update.description,
        completed=task_update.completed
    )

    updated_task = await TaskController.update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        task_update=task_update
    )

    if not updated_task:
        raise TaskNotFoundError(task_id)

    task_response = TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )

    return TaskSingleResponse(data=task_response)


@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for the authenticated user
    """
    success = await TaskController.delete_task(session, task_id, user_id)

    if not success:
        raise TaskNotFoundError(task_id)

    return SuccessResponse()


@router.patch("/{task_id}/complete", response_model=TaskSingleResponse)
async def toggle_task_completion(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    if task_update.completed is None:
        raise ValidationError("Completion status must be provided")

    updated_task = await TaskController.toggle_completion(
        session=session,
        task_id=task_id,
        user_id=user_id,
        completed=task_update.completed
    )

    if not updated_task:
        raise TaskNotFoundError(task_id)

    task_response = TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )

    return TaskSingleResponse(data=task_response)