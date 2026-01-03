from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from enum import Enum

Base = declarative_base()

class PriorityEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(Base):
    """
    Represents a single task in the system.

    Fields:
    - id (Integer): Unique identifier for the task
    - title (String): Title of the task
    - description (Text): Detailed description of the task
    - completed (Boolean): Whether the task is completed
    - created_at (DateTime): Timestamp when the task was created
    - updated_at (DateTime): Timestamp when the task was last updated
    - due_date (Date, nullable): Date when the task is due
    - due_time (Time, nullable): Time when the task is due
    - priority (Enum): Priority level (low, medium, high)
    - is_recurring (Boolean): Whether this task is recurring
    - user_id (Integer): Reference to the user who owns the task
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    due_date = Column(Date)
    due_time = Column(Time)
    priority = Column(String(10), default=PriorityEnum.MEDIUM.value)
    is_recurring = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")
    reminders = relationship("TaskReminder", back_populates="task", cascade="all, delete-orphan")
    recurring_config = relationship("RecurringTask", back_populates="task", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

    def validate(self):
        """Validate the task according to the specification rules."""
        errors = []

        # Title is required and must be between 1-255 characters
        if not self.title or len(self.title) < 1 or len(self.title) > 255:
            errors.append("Title is required and must be between 1-255 characters")

        # Priority must be one of the allowed values
        if self.priority not in [e.value for e in PriorityEnum]:
            errors.append(f"Priority must be one of: {[e.value for e in PriorityEnum]}")

        # If due_date is set, it must be a valid future date
        if self.due_date and self.due_date < datetime.utcnow().date():
            errors.append("Due date must be a valid future date")

        # If due_time is set, due_date must also be set
        if self.due_time and not self.due_date:
            errors.append("If due_time is set, due_date must also be set")

        return errors