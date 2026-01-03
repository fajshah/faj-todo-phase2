from celery import Celery
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.services.reminder_service import ReminderService
from src.services.notification_service import NotificationService
from src.models.task_reminder import TaskReminder
from src.models.task import Task
import os

# Initialize Celery
celery_app = Celery('reminder_scheduler')
celery_app.conf.broker_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("REDIS_URL", "redis://localhost:6379")

@celery_app.task
def check_and_send_reminders():
    """
    Background task to check for upcoming reminders and send notifications.
    """
    db: Session = SessionLocal()
    try:
        # Get upcoming reminders
        reminder_service = ReminderService(db)
        upcoming_reminders = reminder_service.get_upcoming_reminders(limit=100)
        
        # For each upcoming reminder, send notification
        notification_service = NotificationService(
            vapid_private_key=os.environ.get("WEB_PUSH_PRIVATE_KEY", ""),
            vapid_public_key=os.environ.get("WEB_PUSH_PUBLIC_KEY", ""),
            vapid_subject="mailto:admin@example.com"
        )
        
        for reminder in upcoming_reminders:
            # Get the associated task
            task = db.query(Task).filter(Task.id == reminder.task_id).first()
            if not task:
                continue  # Skip if task doesn't exist
            
            # In a real implementation, you would get the user's subscription info
            # For now, we'll simulate sending the notification
            # subscription_info = get_user_subscription(task.user_id)
            
            # For this example, we'll just mark the reminder as sent
            reminder_service.mark_reminder_as_sent(reminder.id)
            
    except Exception as e:
        print(f"Error in check_and_send_reminders: {str(e)}")
    finally:
        db.close()

@celery_app.task
def process_recurring_tasks():
    """
    Background task to process recurring tasks and create new instances.
    """
    db: Session = SessionLocal()
    try:
        # In a real implementation, you would check for recurring tasks
        # that need to generate new instances based on their schedule
        # For now, this is a placeholder
        pass
    except Exception as e:
        print(f"Error in process_recurring_tasks: {str(e)}")
    finally:
        db.close()

# Schedule the tasks to run periodically
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'check-reminders': {
        'task': 'src.background.reminder_scheduler.check_and_send_reminders',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    },
    'process-recurring-tasks': {
        'task': 'src.background.reminder_scheduler.process_recurring_tasks',
        'schedule': crontab(minute=0, hour='*/1'),  # Run every hour
    },
}