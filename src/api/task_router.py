from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from src.database import get_db
from src.models.task import Task
from src.models.recurring_task import RecurringTask
from src.services.recurring_task_service import RecurringTaskService

router = APIRouter()

@router.post("/recurring-tasks", response_model=dict)
def create_recurring_task(
    task_id: int,
    recurrence_type: str,
    recurrence_days: Optional[List[str]] = None,
    end_date: Optional[str] = None,  # Format: "YYYY-MM-DD"
    max_occurrences: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Create a new recurring task configuration based on an existing task
    """
    service = RecurringTaskService(db)
    
    try:
        # Convert end_date string to date object if provided
        from datetime import datetime
        parsed_end_date = None
        if end_date:
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        recurring_task = service.create_recurring_task(
            task_id=task_id,
            recurrence_type=recurrence_type,
            recurrence_days=recurrence_days,
            end_date=parsed_end_date,
            max_occurrences=max_occurrences
        )
        
        return {
            "id": recurring_task.id,
            "task_id": recurring_task.task_id,
            "recurrence_type": recurring_task.recurrence_type,
            "recurrence_days": recurring_task.recurrence_days_list,
            "next_due_date": recurring_task.next_due_date.isoformat() if recurring_task.next_due_date else None,
            "end_date": recurring_task.end_date.isoformat() if recurring_task.end_date else None,
            "max_occurrences": recurring_task.max_occurrences,
            "created_at": recurring_task.created_at.isoformat(),
            "updated_at": recurring_task.updated_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/recurring-tasks/{recurring_task_id}", response_model=dict)
def get_recurring_task(recurring_task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific recurring task configuration
    """
    service = RecurringTaskService(db)
    
    recurring_task = service.get_recurring_task(recurring_task_id)
    if not recurring_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring task configuration not found")
    
    return {
        "id": recurring_task.id,
        "task_id": recurring_task.task_id,
        "recurrence_type": recurring_task.recurrence_type,
        "recurrence_days": recurring_task.recurrence_days_list,
        "next_due_date": recurring_task.next_due_date.isoformat() if recurring_task.next_due_date else None,
        "end_date": recurring_task.end_date.isoformat() if recurring_task.end_date else None,
        "max_occurrences": recurring_task.max_occurrences,
        "created_at": recurring_task.created_at.isoformat(),
        "updated_at": recurring_task.updated_at.isoformat()
    }


@router.put("/recurring-tasks/{recurring_task_id}", response_model=dict)
def update_recurring_task(
    recurring_task_id: int,
    recurrence_type: Optional[str] = None,
    recurrence_days: Optional[List[str]] = None,
    end_date: Optional[str] = None,  # Format: "YYYY-MM-DD"
    max_occurrences: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing recurring task configuration
    """
    service = RecurringTaskService(db)
    
    try:
        # Convert end_date string to date object if provided
        from datetime import datetime
        parsed_end_date = None
        if end_date:
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        updated_task = service.update_recurring_task(
            recurring_task_id=recurring_task_id,
            recurrence_type=recurrence_type,
            recurrence_days=recurrence_days,
            end_date=parsed_end_date,
            max_occurrences=max_occurrences
        )
        
        if not updated_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring task configuration not found")
        
        return {
            "id": updated_task.id,
            "task_id": updated_task.task_id,
            "recurrence_type": updated_task.recurrence_type,
            "recurrence_days": updated_task.recurrence_days_list,
            "next_due_date": updated_task.next_due_date.isoformat() if updated_task.next_due_date else None,
            "end_date": updated_task.end_date.isoformat() if updated_task.end_date else None,
            "max_occurrences": updated_task.max_occurrences,
            "created_at": updated_task.created_at.isoformat(),
            "updated_at": updated_task.updated_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/recurring-tasks/{recurring_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring_task(recurring_task_id: int, db: Session = Depends(get_db)):
    """
    Disable recurrence for a task (does not delete the original task)
    """
    service = RecurringTaskService(db)
    
    success = service.delete_recurring_task(recurring_task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring task configuration not found")
    
    return