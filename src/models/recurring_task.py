from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import json

Base = declarative_base()

class RecurringTask(Base):
    """
    Represents the recurrence configuration for a recurring task.
    
    Fields:
    - id (Integer): Unique identifier for the recurrence configuration
    - task_id (Integer): Reference to the original task
    - recurrence_type (Enum): Type of recurrence (daily, weekly, monthly)
    - recurrence_days (JSON/Array, nullable): Days of the week for weekly recurrence (e.g., ["monday", "wednesday", "friday"])
    - next_due_date (Date): The next date when this task is due
    - end_date (Date, nullable): Date when recurrence should end (optional)
    - max_occurrences (Integer, nullable): Maximum number of occurrences (optional)
    - created_at (DateTime): Timestamp when the recurrence was created
    - updated_at (DateTime): Timestamp when the recurrence was last updated
    """
    
    __tablename__ = "recurring_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, unique=True)
    recurrence_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    recurrence_days = Column(String)  # JSON string for days of the week
    next_due_date = Column(Date, nullable=False)
    end_date = Column(Date)
    max_occurrences = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    task = relationship("Task", back_populates="recurring_config")
    instances = relationship("TaskInstance", back_populates="recurring_task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RecurringTask(id={self.id}, task_id={self.task_id}, recurrence_type='{self.recurrence_type}')>"
    
    @property
    def recurrence_days_list(self):
        """Get recurrence days as a list."""
        if self.recurrence_days:
            return json.loads(self.recurrence_days)
        return []
    
    @recurrence_days_list.setter
    def recurrence_days_list(self, value):
        """Set recurrence days from a list."""
        self.recurrence_days = json.dumps(value) if value else None
    
    def validate(self):
        """Validate the recurring task according to the specification rules."""
        errors = []
        
        # recurrence_type must be one of the allowed values
        allowed_types = ["daily", "weekly", "monthly"]
        if self.recurrence_type not in allowed_types:
            errors.append(f"Recurrence type must be one of: {allowed_types}")
        
        # If recurrence_type is "weekly", recurrence_days must contain valid day names
        if self.recurrence_type == "weekly":
            if not self.recurrence_days_list:
                errors.append("Weekly recurrence must specify days of the week")
            else:
                valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                invalid_days = [day for day in self.recurrence_days_list if day.lower() not in valid_days]
                if invalid_days:
                    errors.append(f"Invalid days for weekly recurrence: {invalid_days}")
        
        # next_due_date must be a valid future date
        if self.next_due_date and self.next_due_date < datetime.utcnow().date():
            errors.append("Next due date must be a valid future date")
        
        # end_date must be after the current date if specified
        if self.end_date and self.end_date < datetime.utcnow().date():
            errors.append("End date must be after the current date")
        
        # max_occurrences must be a positive integer if specified
        if self.max_occurrences is not None and self.max_occurrences <= 0:
            errors.append("Max occurrences must be a positive integer")
        
        return errors