from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.task import Task
from src.models.task_reminder import TaskReminder
from datetime import datetime, timedelta
import pytz

class ReminderService:
    """
    Service class to handle task reminder operations.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def schedule_reminder(
        self,
        task_id: int,
        reminder_time: datetime,
        notification_type: str = "browser"
    ) -> TaskReminder:
        """
        Schedule a reminder for a specific task.
        
        Args:
            task_id: ID of the task to schedule a reminder for
            reminder_time: When the reminder should be sent
            notification_type: Type of notification ('browser', 'email', etc.)
            
        Returns:
            The created TaskReminder object
        """
        # Get the task
        task = self.db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        # Check if a reminder already exists for this task at this time
        existing_reminder = self.db_session.query(TaskReminder).filter(
            TaskReminder.task_id == task_id,
            TaskReminder.reminder_time == reminder_time
        ).first()
        if existing_reminder:
            raise ValueError(f"Reminder already exists for task {task_id} at {reminder_time}")
        
        # Create the reminder
        reminder = TaskReminder(
            task_id=task_id,
            reminder_time=reminder_time,
            notification_type=notification_type
        )
        
        # Validate the reminder
        validation_errors = reminder.validate()
        if validation_errors:
            raise ValueError(f"Invalid reminder configuration: {validation_errors}")
        
        # Check that reminder time is not in the past
        if reminder_time < datetime.utcnow():
            raise ValueError("Reminder time cannot be in the past")
        
        # Check that reminder time is before the task's due time
        if task.due_date:
            task_due_datetime = datetime.combine(task.due_date, task.due_time or datetime.min.time())
            if reminder_time >= task_due_datetime:
                raise ValueError("Reminder time must be before the task's due time")
        
        # Add to the database
        self.db_session.add(reminder)
        self.db_session.commit()
        self.db_session.refresh(reminder)
        
        return reminder
    
    def get_reminder(self, reminder_id: int) -> Optional[TaskReminder]:
        """
        Get a specific reminder by ID.
        
        Args:
            reminder_id: ID of the reminder
            
        Returns:
            The TaskReminder object or None if not found
        """
        return self.db_session.query(TaskReminder).filter(
            TaskReminder.id == reminder_id
        ).first()
    
    def get_reminders_for_task(self, task_id: int) -> List[TaskReminder]:
        """
        Get all reminders for a specific task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            List of TaskReminder objects for the task
        """
        return self.db_session.query(TaskReminder).filter(
            TaskReminder.task_id == task_id
        ).all()
    
    def get_upcoming_reminders(self, limit: int = 10) -> List[TaskReminder]:
        """
        Get upcoming reminders (for the next 24 hours by default).
        
        Args:
            limit: Maximum number of reminders to return
            
        Returns:
            List of upcoming TaskReminder objects
        """
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        
        return self.db_session.query(TaskReminder).filter(
            TaskReminder.reminder_time >= now,
            TaskReminder.reminder_time <= tomorrow,
            TaskReminder.sent == False
        ).order_by(TaskReminder.reminder_time).limit(limit).all()
    
    def mark_reminder_as_sent(self, reminder_id: int) -> Optional[TaskReminder]:
        """
        Mark a reminder as sent.
        
        Args:
            reminder_id: ID of the reminder to mark as sent
            
        Returns:
            The updated TaskReminder object or None if not found
        """
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            return None
        
        reminder.sent = True
        reminder.sent_at = datetime.utcnow()
        
        self.db_session.commit()
        self.db_session.refresh(reminder)
        
        return reminder
    
    def cancel_reminder(self, reminder_id: int) -> bool:
        """
        Cancel a scheduled reminder.
        
        Args:
            reminder_id: ID of the reminder to cancel
            
        Returns:
            True if canceled, False if not found
        """
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            return False
        
        self.db_session.delete(reminder)
        self.db_session.commit()
        return True