from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class TaskInstance(Base):
    """
    Represents a specific occurrence of a recurring task.
    
    Fields:
    - id (Integer): Unique identifier for the instance
    - original_task_id (Integer): Reference to the original recurring task
    - instance_due_date (Date): Due date for this specific instance
    - instance_due_time (Time, nullable): Due time for this specific instance
    - completed (Boolean): Whether this instance is completed
    - created_at (DateTime): Timestamp when the instance was created
    - completed_at (DateTime, nullable): When this instance was completed
    """
    
    __tablename__ = "task_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    original_task_id = Column(Integer, ForeignKey("recurring_tasks.id"), nullable=False)
    instance_due_date = Column(Date, nullable=False)
    instance_due_time = Column(Time)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    
    # Relationship
    recurring_task = relationship("RecurringTask", back_populates="instances")
    
    def __repr__(self):
        return f"<TaskInstance(id={self.id}, original_task_id={self.original_task_id}, instance_due_date={self.instance_due_date}, completed={self.completed})>"
    
    def validate(self):
        """Validate the task instance according to the specification rules."""
        errors = []
        
        # instance_due_date must be a valid date
        if not self.instance_due_date:
            errors.append("Instance due date must be a valid date")
        
        # completed_at can only be set if completed is true
        if self.completed_at and not self.completed:
            errors.append("Completed at can only be set if completed is true")
        
        return errors