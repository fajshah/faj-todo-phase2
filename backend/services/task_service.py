from typing import List, Optional
from sqlmodel import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from models.task import Task, TaskCreate, TaskUpdate
from schemas.task import TaskStatus

class TaskService:
    """
    Service class for handling task business logic
    """

    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
        """
        Create a new task for a user
        """
        # Create task instance
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=task_data.user_id
        )

        # Add to session and commit
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def get_tasks(
        session: AsyncSession,
        user_id: str,
        status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional status filtering
        """
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if specified
        if status and status != TaskStatus.all:
            if status == TaskStatus.pending:
                query = query.where(Task.completed == False)
            elif status == TaskStatus.completed:
                query = query.where(Task.completed == True)

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        return tasks

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a specific user (ensures ownership)
        """
        query = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: int,
        user_id: str,
        task_update: TaskUpdate
    ) -> Optional[Task]:
        """
        Update a specific task for a user (ensures ownership)
        """
        # Get the task to update
        db_task = await TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Update fields that were provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        # Commit changes
        await session.commit()
        await session.refresh(db_task)

        return db_task

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for a user (ensures ownership)
        """
        # Get the task to delete
        db_task = await TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return False

        # Delete the task
        await session.delete(db_task)
        await session.commit()

        return True

    @staticmethod
    async def toggle_completion(
        session: AsyncSession,
        task_id: int,
        user_id: str,
        completed: bool
    ) -> Optional[Task]:
        """
        Toggle the completion status of a task for a user (ensures ownership)
        """
        # Get the task to update
        db_task = await TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Update the completion status
        db_task.completed = completed
        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        # Commit changes
        await session.commit()
        await session.refresh(db_task)

        return db_task