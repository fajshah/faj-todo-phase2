from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from src.database import get_db
from src.models.task import Task
from src.models.task_reminder import TaskReminder
from src.services.reminder_service import ReminderService

router = APIRouter()

@router.post("/reminders", response_model=dict)
def schedule_reminder(
    task_id: int,
    reminder_time: str,  # Format: "YYYY-MM-DDTHH:MM:SS" (ISO format)
    notification_type: str = "browser",
    db: Session = Depends(get_db)
):
    """
    Schedule a reminder for a specific task
    """
    service = ReminderService(db)
    
    try:
        # Parse the reminder time from ISO format string
        from datetime import datetime
        parsed_reminder_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
        
        reminder = service.schedule_reminder(
            task_id=task_id,
            reminder_time=parsed_reminder_time,
            notification_type=notification_type
        )
        
        return {
            "id": reminder.id,
            "task_id": reminder.task_id,
            "reminder_time": reminder.reminder_time.isoformat(),
            "sent": reminder.sent,
            "sent_at": reminder.sent_at.isoformat() if reminder.sent_at else None,
            "notification_type": reminder.notification_type,
            "created_at": reminder.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/reminders/{reminder_id}", response_model=dict)
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific reminder
    """
    service = ReminderService(db)
    
    reminder = service.get_reminder(reminder_id)
    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    
    return {
        "id": reminder.id,
        "task_id": reminder.task_id,
        "reminder_time": reminder.reminder_time.isoformat(),
        "sent": reminder.sent,
        "sent_at": reminder.sent_at.isoformat() if reminder.sent_at else None,
        "notification_type": reminder.notification_type,
        "created_at": reminder.created_at.isoformat()
    }


@router.get("/reminders", response_model=List[dict])
def get_reminders_for_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all reminders for a specific task
    """
    service = ReminderService(db)
    
    reminders = service.get_reminders_for_task(task_id)
    
    return [
        {
            "id": reminder.id,
            "task_id": reminder.task_id,
            "reminder_time": reminder.reminder_time.isoformat(),
            "sent": reminder.sent,
            "sent_at": reminder.sent_at.isoformat() if reminder.sent_at else None,
            "notification_type": reminder.notification_type,
            "created_at": reminder.created_at.isoformat()
        }
        for reminder in reminders
    ]


@router.get("/reminders/upcoming", response_model=List[dict])
def get_upcoming_reminders(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve upcoming reminders (for the next 24 hours by default)
    """
    service = ReminderService(db)
    
    reminders = service.get_upcoming_reminders(limit)
    
    return [
        {
            "id": reminder.id,
            "task_id": reminder.task_id,
            "reminder_time": reminder.reminder_time.isoformat(),
            "sent": reminder.sent,
            "sent_at": reminder.sent_at.isoformat() if reminder.sent_at else None,
            "notification_type": reminder.notification_type,
            "created_at": reminder.created_at.isoformat()
        }
        for reminder in reminders
    ]


@router.put("/reminders/{reminder_id}/sent", response_model=dict)
def mark_reminder_as_sent(reminder_id: int, db: Session = Depends(get_db)):
    """
    Mark a reminder as sent (used by the background job)
    """
    service = ReminderService(db)
    
    reminder = service.mark_reminder_as_sent(reminder_id)
    if not reminder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    
    return {
        "id": reminder.id,
        "task_id": reminder.task_id,
        "reminder_time": reminder.reminder_time.isoformat(),
        "sent": reminder.sent,
        "sent_at": reminder.sent_at.isoformat() if reminder.sent_at else None,
        "notification_type": reminder.notification_type,
        "created_at": reminder.created_at.isoformat()
    }


@router.delete("/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """
    Cancel a scheduled reminder
    """
    service = ReminderService(db)
    
    success = service.cancel_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    
    return