from celery import Celery
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.services.recurring_task_service import RecurringTaskService
from src.models.task import Task
import os

# Initialize Celery (reuse the same instance from reminder_scheduler)
celery_app = Celery('recurring_task_handler')
celery_app.conf.broker_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("REDIS_URL", "redis://localhost:6379")

@celery_app.task
def handle_completed_recurring_task(task_id: int):
    """
    Background task to handle a completed recurring task and create the next instance.
    """
    db: Session = SessionLocal()
    try:
        # Create the recurring task service
        recurring_task_service = RecurringTaskService(db)
        
        # Create the next task instance
        next_instance = recurring_task_service.create_next_task_instance(task_id)
        
        if next_instance:
            print(f"Created next task instance for task {task_id}: {next_instance.id}")
        else:
            print(f"No next instance created for task {task_id} - recurrence may have ended")
            
    except Exception as e:
        print(f"Error in handle_completed_recurring_task for task {task_id}: {str(e)}")
    finally:
        db.close()