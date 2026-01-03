"""
Core business logic for the Todo application.
This module contains shared logic between the FastAPI web API and CLI application.
"""
from typing import List, Optional
from datetime import datetime, date, time
from enum import Enum
from dataclasses import dataclass


class PriorityEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    is_recurring: bool = False
    user_id: Optional[int] = None


@dataclass
class RecurringTask:
    id: int
    task_id: int
    recurrence_type: str  # daily, weekly, monthly
    recurrence_days: Optional[List[str]] = None  # For weekly recurrence
    next_due_date: Optional[date] = None
    end_date: Optional[date] = None
    max_occurrences: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TodoCore:
    """
    Core business logic for todo operations.
    This class contains shared logic between the FastAPI web API and CLI application.
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using in-memory storage for demonstration
        self.tasks: List[Task] = []
        self.recurring_tasks: List[RecurringTask] = []
        self._next_task_id = 1
        self._next_recurring_id = 1
    
    def add_task(
        self, 
        title: str, 
        description: Optional[str] = None,
        due_date: Optional[date] = None,
        due_time: Optional[time] = None,
        priority: PriorityEnum = PriorityEnum.MEDIUM,
        is_recurring: bool = False
    ) -> Task:
        """Add a new task."""
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        
        task = Task(
            id=self._next_task_id,
            title=title,
            description=description,
            due_date=due_date,
            due_time=due_time,
            priority=priority,
            is_recurring=is_recurring,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.tasks.append(task)
        self._next_task_id += 1
        return task
    
    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        """List all tasks, optionally filtering out completed ones."""
        if include_completed:
            return self.tasks[:]
        return [task for task in self.tasks if not task.completed]
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def complete_task(self, task_id: int, completed: bool = True) -> Optional[Task]:
        """Mark a task as completed or incomplete."""
        task = self.get_task(task_id)
        if task:
            task.completed = completed
            task.updated_at = datetime.now()
            return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            # Also remove any associated recurring task configuration
            self.recurring_tasks = [rt for rt in self.recurring_tasks if rt.task_id != task_id]
            return True
        return False
    
    def add_recurring_task(
        self,
        task_id: int,
        recurrence_type: str,
        recurrence_days: Optional[List[str]] = None,
        end_date: Optional[date] = None,
        max_occurrences: Optional[int] = None
    ) -> Optional[RecurringTask]:
        """Add a recurring task configuration."""
        # Validate recurrence type
        valid_types = ["daily", "weekly", "monthly"]
        if recurrence_type not in valid_types:
            raise ValueError(f"Recurrence type must be one of: {valid_types}")
        
        # Validate recurrence days for weekly type
        if recurrence_type == "weekly":
            if not recurrence_days:
                raise ValueError("Weekly recurrence requires at least one day")
            
            valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            invalid_days = [day for day in recurrence_days if day.lower() not in valid_days]
            if invalid_days:
                raise ValueError(f"Invalid days for weekly recurrence: {invalid_days}")
        
        # Check if task exists
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")
        
        # Check if task already has a recurring configuration
        existing_config = self.get_recurring_task_for_task(task_id)
        if existing_config:
            raise ValueError(f"Task with ID {task_id} already has a recurring configuration")
        
        # Create recurring task
        recurring_task = RecurringTask(
            id=self._next_recurring_id,
            task_id=task_id,
            recurrence_type=recurrence_type,
            recurrence_days=recurrence_days,
            next_due_date=task.due_date if task.due_date else date.today(),
            end_date=end_date,
            max_occurrences=max_occurrences,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.recurring_tasks.append(recurring_task)
        self._next_recurring_id += 1
        
        # Update the original task to mark it as recurring
        task.is_recurring = True
        return recurring_task
    
    def get_recurring_task_for_task(self, task_id: int) -> Optional[RecurringTask]:
        """Get the recurring task configuration for a specific task."""
        for rt in self.recurring_tasks:
            if rt.task_id == task_id:
                return rt
        return None
    
    def get_recurring_task(self, recurring_task_id: int) -> Optional[RecurringTask]:
        """Get a recurring task configuration by ID."""
        for rt in self.recurring_tasks:
            if rt.id == recurring_task_id:
                return rt
        return None
    
    def list_recurring_tasks(self) -> List[RecurringTask]:
        """List all recurring task configurations."""
        return self.recurring_tasks[:]
    
    def delete_recurring_task(self, recurring_task_id: int) -> bool:
        """Delete a recurring task configuration."""
        recurring_task = self.get_recurring_task(recurring_task_id)
        if recurring_task:
            self.recurring_tasks.remove(recurring_task)
            
            # Update the original task to mark it as non-recurring
            task = self.get_task(recurring_task.task_id)
            if task:
                task.is_recurring = False
            
            return True
        return False