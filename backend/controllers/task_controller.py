from typing import List, Optional
from services.task_service import TaskService
from models.task import Task, TaskCreate, TaskUpdate
from schemas.task import TaskStatus
from sqlmodel.ext.asyncio.session import AsyncSession

class TaskController:
    """
    Controller class for handling task business logic
    """

    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
        """
        Create a new task
        """
        return await TaskService.create_task(session, task_data)

    @staticmethod
    async def get_tasks(
        session: AsyncSession,
        user_id: str,
        status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """
        Get all tasks for a user with optional status filtering
        """
        return await TaskService.get_tasks(session, user_id, status)

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a user
        """
        return await TaskService.get_task_by_id(session, task_id, user_id)

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: int,
        user_id: str,
        task_update: TaskUpdate
    ) -> Optional[Task]:
        """
        Update a specific task for a user
        """
        return await TaskService.update_task(session, task_id, user_id, task_update)

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for a user
        """
        return await TaskService.delete_task(session, task_id, user_id)

    @staticmethod
    async def toggle_completion(
        session: AsyncSession,
        task_id: int,
        user_id: str,
        completed: bool
    ) -> Optional[Task]:
        """
        Toggle the completion status of a task for a user
        """
        return await TaskService.toggle_completion(session, task_id, user_id, completed)