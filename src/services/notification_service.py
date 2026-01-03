import pywebpush
import json
from typing import Optional
from src.models.task_reminder import TaskReminder
from src.models.task import Task
from sqlalchemy.orm import Session

class NotificationService:
    """
    Service class to handle browser notifications.
    """
    
    def __init__(self, vapid_private_key: str, vapid_public_key: str, vapid_subject: str = "mailto:test@example.com"):
        self.vapid_private_key = vapid_private_key
        self.vapid_public_key = vapid_public_key
        self.vapid_subject = vapid_subject
    
    def send_browser_notification(
        self,
        subscription_info: dict,
        task: Task,
        reminder: TaskReminder
    ) -> bool:
        """
        Send a browser notification for a task reminder.
        
        Args:
            subscription_info: Web push subscription information
            task: The task associated with the reminder
            reminder: The reminder that triggered the notification
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        try:
            # Prepare the notification payload
            payload = {
                "title": f"Task Reminder: {task.title}",
                "body": f"Your task '{task.title}' is due soon!",
                "icon": "/icon.png",  # Default icon path
                "badge": "/badge.png",  # Default badge path
                "data": {
                    "task_id": task.id,
                    "reminder_id": reminder.id,
                    "due_date": str(task.due_date) if task.due_date else None,
                    "due_time": str(task.due_time) if task.due_time else None
                }
            }
            
            # Send the web push notification
            pywebpush.send_webpush(
                subscription=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=self.vapid_private_key,
                vapid_claims={
                    "sub": self.vapid_subject
                }
            )
            
            return True
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")
            return False
    
    def format_notification_message(self, task: Task) -> str:
        """
        Format the notification message for a task.
        
        Args:
            task: The task to format a message for
            
        Returns:
            Formatted notification message
        """
        message = f"Task Reminder: {task.title}"
        
        if task.due_date:
            message += f" is due on {task.due_date}"
            if task.due_time:
                message += f" at {task.due_time}"
        
        if task.priority:
            message += f" (Priority: {task.priority})"
        
        return message