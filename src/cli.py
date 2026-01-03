"""
Command Line Interface for the Todo application.
This module provides a CLI interface that uses the same core logic as the FastAPI web API.
"""
import typer
from typing import Optional, List
from datetime import datetime, date
import sys

from src.core.todo_core import TodoCore, Task, RecurringTask, PriorityEnum

# Create Typer app
app = typer.Typer(name="todo", help="A command-line todo application")

# Initialize the core logic
todo_core = TodoCore()


@app.command()
def add(
    title: str = typer.Argument(..., help="Title of the task"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description of the task"),
    due_date: Optional[str] = typer.Option(None, "--due-date", help="Due date in YYYY-MM-DD format"),
    due_time: Optional[str] = typer.Option(None, "--due-time", help="Due time in HH:MM format"),
    priority: PriorityEnum = typer.Option(PriorityEnum.MEDIUM, "--priority", "-p", help="Priority level"),
    recurring: bool = typer.Option(False, "--recurring", "-r", help="Mark task as recurring")
):
    """
    Add a new task to your todo list.
    """
    # Parse due date if provided
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo(f"Error: Invalid date format '{due_date}'. Use YYYY-MM-DD.", err=True)
            sys.exit(1)
    
    # Parse due time if provided
    parsed_due_time = None
    if due_time:
        try:
            parsed_due_time = datetime.strptime(due_time, "%H:%M").time()
        except ValueError:
            typer.echo(f"Error: Invalid time format '{due_time}'. Use HH:MM.", err=True)
            sys.exit(1)
    
    try:
        task = todo_core.add_task(
            title=title,
            description=description,
            due_date=parsed_due_date,
            due_time=parsed_due_time,
            priority=priority,
            is_recurring=recurring
        )
        typer.echo(f"Added task: {task.title} (ID: {task.id})")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@app.command(name="list")
def list_tasks(
    show_completed: bool = typer.Option(True, "--all", "-a", help="Show completed tasks as well"),
    show_recurring: bool = typer.Option(False, "--recurring", "-r", help="Show only recurring tasks")
):
    """
    List all tasks in your todo list.
    """
    tasks = todo_core.list_tasks(include_completed=show_completed)
    
    if show_recurring:
        tasks = [task for task in tasks if task.is_recurring]
    
    if not tasks:
        typer.echo("No tasks found.")
        return
    
    # Print tasks in a formatted table
    typer.echo(f"{'ID':<4} {'Status':<10} {'Title':<30} {'Due Date':<12} {'Priority':<10} {'Recurring':<10}")
    typer.echo("-" * 80)
    
    for task in tasks:
        status = "✓" if task.completed else "○"
        due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
        priority_str = task.priority.value
        recurring_str = "Yes" if task.is_recurring else "No"
        
        # Truncate title if too long
        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
        
        typer.echo(f"{task.id:<4} {status:<10} {title:<30} {due_date_str:<12} {priority_str:<10} {recurring_str:<10}")


@app.command()
def complete(task_id: int = typer.Argument(..., help="ID of the task to complete")):
    """
    Mark a task as completed.
    """
    task = todo_core.complete_task(task_id, completed=True)
    if task:
        typer.echo(f"Completed task: {task.title}")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.", err=True)
        sys.exit(1)


@app.command()
def uncomplete(task_id: int = typer.Argument(..., help="ID of the task to mark as incomplete")):
    """
    Mark a task as incomplete.
    """
    task = todo_core.complete_task(task_id, completed=False)
    if task:
        typer.echo(f"Marked task as incomplete: {task.title}")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.", err=True)
        sys.exit(1)


@app.command()
def delete(task_id: int = typer.Argument(..., help="ID of the task to delete")):
    """
    Delete a task from your todo list.
    """
    if todo_core.delete_task(task_id):
        typer.echo(f"Deleted task with ID {task_id}")
    else:
        typer.echo(f"Error: Task with ID {task_id} not found.", err=True)
        sys.exit(1)


# Recurring tasks subcommands
recurring_app = typer.Typer(name="recurring", help="Manage recurring tasks")
app.add_typer(recurring_app, name="recurring")


@recurring_app.command(name="add")
def recurring_add(
    task_id: int = typer.Argument(..., help="ID of the task to make recurring"),
    recurrence_type: str = typer.Option(..., "--type", "-t", help="Recurrence type: daily, weekly, monthly"),
    days: Optional[str] = typer.Option(None, "--days", "-d", help="Comma-separated days for weekly recurrence (e.g., monday,wednesday,friday)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", help="End date in YYYY-MM-DD format"),
    max_occurrences: Optional[int] = typer.Option(None, "--max", help="Maximum number of occurrences")
):
    """
    Make a task recurring.
    """
    # Parse days if provided
    recurrence_days = None
    if days:
        recurrence_days = [day.strip().lower() for day in days.split(",")]
    
    # Parse end date if provided
    parsed_end_date = None
    if end_date:
        try:
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo(f"Error: Invalid date format '{end_date}'. Use YYYY-MM-DD.", err=True)
            sys.exit(1)
    
    try:
        recurring_task = todo_core.add_recurring_task(
            task_id=task_id,
            recurrence_type=recurrence_type.lower(),
            recurrence_days=recurrence_days,
            end_date=parsed_end_date,
            max_occurrences=max_occurrences
        )
        typer.echo(f"Added recurring task configuration for task {task_id}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@recurring_app.command(name="list")
def recurring_list():
    """
    List all recurring task configurations.
    """
    recurring_tasks = todo_core.list_recurring_tasks()
    
    if not recurring_tasks:
        typer.echo("No recurring tasks configured.")
        return
    
    # Print recurring tasks in a formatted table
    typer.echo(f"{'ID':<4} {'Task ID':<8} {'Type':<10} {'Days':<20} {'Next Due':<12} {'End Date':<12}")
    typer.echo("-" * 70)
    
    for rt in recurring_tasks:
        days_str = ", ".join(rt.recurrence_days) if rt.recurrence_days else ""
        next_due_str = rt.next_due_date.strftime("%Y-%m-%d") if rt.next_due_date else ""
        end_date_str = rt.end_date.strftime("%Y-%m-%d") if rt.end_date else ""
        
        typer.echo(f"{rt.id:<4} {rt.task_id:<8} {rt.recurrence_type:<10} {days_str:<20} {next_due_str:<12} {end_date_str:<12}")


@recurring_app.command(name="delete")
def recurring_delete(recurring_id: int = typer.Argument(..., help="ID of the recurring task configuration to delete")):
    """
    Delete a recurring task configuration.
    """
    if todo_core.delete_recurring_task(recurring_id):
        typer.echo(f"Deleted recurring task configuration with ID {recurring_id}")
    else:
        typer.echo(f"Error: Recurring task configuration with ID {recurring_id} not found.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()