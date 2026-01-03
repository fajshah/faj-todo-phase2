from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class TaskReminder(Base):
    """
    Represents a scheduled reminder for a task.
    
    Fields:
    - id (Integer): Unique identifier for the reminder
    - task_id (Integer): Reference to the task
    - reminder_time (DateTime): When the reminder should be sent
    - sent (Boolean): Whether the reminder has been sent
    - sent_at (DateTime, nullable): When the reminder was actually sent
    - notification_type (Enum): Type of notification (browser, email, etc.)
    - created_at (DateTime): Timestamp when the reminder was created
    """
    
    __tablename__ = "task_reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    notification_type = Column(String(20), default="browser")  # browser, email, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    task = relationship("Task", back_populates="reminders")
    
    def __repr__(self):
        return f"<TaskReminder(id={self.id}, task_id={self.task_id}, reminder_time={self.reminder_time}, sent={self.sent})>"
    
    def validate(self):
        """Validate the reminder according to the specification rules."""
        errors = []
        
        # reminder_time must be before the task's due_time
        # This would require accessing the related task, which we'll handle in the service layer
        
        # notification_type must be one of the allowed values
        allowed_types = ["browser", "email"]
        if self.notification_type not in allowed_types:
            errors.append(f"Notification type must be one of: {allowed_types}")
        
        # A task cannot have duplicate reminder times
        # This validation would happen at the service level when creating reminders
        
        return errors