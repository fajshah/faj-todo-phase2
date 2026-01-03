from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.task import Task
from src.models.recurring_task import RecurringTask
from src.models.task_instance import TaskInstance
from src.utils.date_utils import calculate_next_due_date, handle_february_29th, _add_months
from datetime import date, timedelta

class RecurringTaskService:
    """
    Service class to handle recurring task operations.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_recurring_task(
        self,
        task_id: int,
        recurrence_type: str,
        recurrence_days: Optional[List[str]] = None,
        end_date: Optional[date] = None,
        max_occurrences: Optional[int] = None
    ) -> RecurringTask:
        """
        Create a new recurring task configuration.

        Args:
            task_id: ID of the base task
            recurrence_type: Type of recurrence ('daily', 'weekly', 'monthly')
            recurrence_days: Days of the week for weekly recurrence
            end_date: Optional end date for the recurrence
            max_occurrences: Optional maximum number of occurrences

        Returns:
            The created RecurringTask object
        """
        # Get the base task
        task = self.db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Check if the task already has a recurring configuration
        existing_config = self.db_session.query(RecurringTask).filter(
            RecurringTask.task_id == task_id
        ).first()
        if existing_config:
            raise ValueError(f"Task with ID {task_id} already has a recurring configuration")

        # Create the recurring task configuration
        recurring_task = RecurringTask(
            task_id=task_id,
            recurrence_type=recurrence_type,
            recurrence_days_list=recurrence_days,
            next_due_date=task.due_date if task.due_date else date.today(),
            end_date=end_date,
            max_occurrences=max_occurrences
        )

        # Validate the recurring task
        validation_errors = recurring_task.validate()
        if validation_errors:
            raise ValueError(f"Invalid recurring task configuration: {validation_errors}")

        # Add to the database
        self.db_session.add(recurring_task)
        self.db_session.commit()
        self.db_session.refresh(recurring_task)

        return recurring_task

    def get_recurring_task(self, recurring_task_id: int) -> Optional[RecurringTask]:
        """
        Get a recurring task configuration by ID.

        Args:
            recurring_task_id: ID of the recurring task

        Returns:
            The RecurringTask object or None if not found
        """
        return self.db_session.query(RecurringTask).filter(
            RecurringTask.id == recurring_task_id
        ).first()

    def update_recurring_task(
        self,
        recurring_task_id: int,
        recurrence_type: Optional[str] = None,
        recurrence_days: Optional[List[str]] = None,
        end_date: Optional[date] = None,
        max_occurrences: Optional[int] = None
    ) -> Optional[RecurringTask]:
        """
        Update an existing recurring task configuration.

        Args:
            recurring_task_id: ID of the recurring task to update
            recurrence_type: New recurrence type
            recurrence_days: New days of the week for weekly recurrence
            end_date: New end date
            max_occurrences: New maximum occurrences

        Returns:
            The updated RecurringTask object or None if not found
        """
        recurring_task = self.get_recurring_task(recurring_task_id)
        if not recurring_task:
            return None

        # Update fields if provided
        if recurrence_type is not None:
            recurring_task.recurrence_type = recurrence_type
        if recurrence_days is not None:
            recurring_task.recurrence_days_list = recurrence_days
        if end_date is not None:
            recurring_task.end_date = end_date
        if max_occurrences is not None:
            recurring_task.max_occurrences = max_occurrences

        # Validate the updated recurring task
        validation_errors = recurring_task.validate()
        if validation_errors:
            raise ValueError(f"Invalid recurring task configuration: {validation_errors}")

        # Update in the database
        self.db_session.commit()
        self.db_session.refresh(recurring_task)

        return recurring_task

    def delete_recurring_task(self, recurring_task_id: int) -> bool:
        """
        Delete a recurring task configuration (disables recurrence).

        Args:
            recurring_task_id: ID of the recurring task to delete

        Returns:
            True if deleted, False if not found
        """
        recurring_task = self.get_recurring_task(recurring_task_id)
        if not recurring_task:
            return False

        self.db_session.delete(recurring_task)
        self.db_session.commit()
        return True

    def create_next_task_instance(self, task_id: int) -> Optional[TaskInstance]:
        """
        Create the next task instance when a recurring task is completed.

        Args:
            task_id: ID of the completed task

        Returns:
            The created TaskInstance object or None if recurrence has ended
        """
        # Get the recurring task configuration
        recurring_task = self.db_session.query(RecurringTask).filter(
            RecurringTask.task_id == task_id
        ).first()

        if not recurring_task:
            return None  # Not a recurring task

        # Calculate the next due date
        next_due_date = calculate_next_due_date(
            recurring_task.next_due_date,
            recurring_task.recurrence_type,
            recurring_task.recurrence_days_list,
            recurring_task.end_date
        )

        # Check if recurrence has ended
        if next_due_date is None:
            # Recurrence has ended, delete the configuration
            self.delete_recurring_task(recurring_task.id)
            return None

        # Create a new task instance
        task_instance = TaskInstance(
            original_task_id=recurring_task.id,
            instance_due_date=next_due_date,
            instance_due_time=recurring_task.task.due_time,  # Use the same due time as the original task
            completed=False
        )

        # Add to the database
        self.db_session.add(task_instance)
        self.db_session.commit()
        self.db_session.refresh(task_instance)

        # Update the next due date in the recurring task configuration
        recurring_task.next_due_date = next_due_date
        self.db_session.commit()

        return task_instance

    def calculate_next_due_date_for_daily(self, current_due_date: date) -> date:
        """
        Calculate the next due date for daily recurrence.

        Args:
            current_due_date: The current due date

        Returns:
            The next due date
        """
        return current_due_date + timedelta(days=1)

    def calculate_next_due_date_for_weekly(
        self,
        current_due_date: date,
        recurrence_days: List[str]
    ) -> date:
        """
        Calculate the next due date for weekly recurrence.

        Args:
            current_due_date: The current due date
            recurrence_days: Days of the week for recurrence

        Returns:
            The next due date
        """
        return calculate_next_due_date(
            current_due_date,
            "weekly",
            recurrence_days
        )

    def calculate_next_due_date_for_monthly(self, current_due_date: date) -> date:
        """
        Calculate the next due date for monthly recurrence.

        Args:
            current_due_date: The current due date

        Returns:
            The next due date
        """
        from src.utils.date_utils import _add_months
        return _add_months(current_due_date, 1)