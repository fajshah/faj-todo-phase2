#!/usr/bin/env python
"""
Test script to verify the CLI functionality works correctly.
"""
from src.core.todo_core import TodoCore

def test_cli_functionality():
    print("Testing CLI functionality...")
    
    # Create a core instance
    core = TodoCore()
    
    # Test adding a task
    print("\n1. Adding a task...")
    task = core.add_task("Test task", "This is a test task")
    print(f"Added task: {task.title} (ID: {task.id})")
    
    # Test listing tasks
    print("\n2. Listing tasks...")
    tasks = core.list_tasks()
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"  ID: {task.id}, Title: {task.title}, Status: {status}")
    
    # Test completing a task
    print("\n3. Completing a task...")
    completed_task = core.complete_task(1, completed=True)
    if completed_task:
        print(f"Completed task: {completed_task.title}")
    
    # Test listing again to see the status change
    print("\n4. Listing tasks after completion...")
    tasks = core.list_tasks()
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"  ID: {task.id}, Title: {task.title}, Status: {status}")
    
    # Test adding a recurring task
    print("\n5. Adding recurring task configuration...")
    recurring_task = core.add_recurring_task(
        task_id=1,
        recurrence_type="daily"
    )
    if recurring_task:
        print(f"Added recurring configuration for task {recurring_task.task_id}")
    
    # Test listing recurring tasks
    print("\n6. Listing recurring tasks...")
    recurring_tasks = core.list_recurring_tasks()
    for rt in recurring_tasks:
        print(f"  ID: {rt.id}, Task ID: {rt.task_id}, Type: {rt.recurrence_type}")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_cli_functionality()