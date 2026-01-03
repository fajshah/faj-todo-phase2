"""
Interactive CLI for the Todo application.
This provides a continuous interactive session like the original console app.
"""
from src.core.todo_core import TodoCore
from datetime import datetime, date
from typing import Optional


def print_help():
    """Print available commands."""
    print("\nAvailable commands:")
    print("  add <title> [description] [priority] - Add a new task")
    print("  list - List all tasks")
    print("  complete <id> - Mark task as complete")
    print("  uncomplete <id> - Mark task as incomplete")
    print("  delete <id> - Delete a task")
    print("  recurring add <id> <type> [days] - Make task recurring")
    print("  recurring list - List recurring tasks")
    print("  recurring delete <id> - Delete recurring task config")
    print("  help - Show this help")
    print("  quit or exit - Exit the application")


def parse_command(user_input: str):
    """Parse user input into command and arguments."""
    parts = user_input.strip().split()
    if not parts:
        return None, []
    
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def interactive_cli():
    """Run the interactive CLI session."""
    print("Welcome to the Interactive Todo CLI!")
    print("Type 'help' for available commands or 'quit' to exit.")
    
    # Initialize the core logic (this will persist for the session)
    todo_core = TodoCore()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
                
            command, args = parse_command(user_input)
            
            if command in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif command == 'help':
                print_help()
            elif command == 'add':
                if len(args) < 1:
                    print("Usage: add <title> [description]")
                    continue
                
                title = args[0]
                description = " ".join(args[1:]) if len(args) > 1 else None
                
                try:
                    task = todo_core.add_task(title=title, description=description)
                    print(f"Added task: {task.title} (ID: {task.id})")
                except ValueError as e:
                    print(f"Error: {e}")
            elif command == 'list':
                tasks = todo_core.list_tasks()
                if not tasks:
                    print("No tasks found.")
                else:
                    print(f"{'ID':<4} {'Status':<10} {'Title':<30} {'Priority':<10}")
                    print("-" * 60)
                    for task in tasks:
                        status = "Completed" if task.completed else "Pending"
                        title = task.title[:27] + "..." if len(task.title) > 30 else task.title
                        print(f"{task.id:<4} {status:<10} {title:<30} {task.priority.value:<10}")
            elif command == 'complete':
                if len(args) < 1:
                    print("Usage: complete <id>")
                    continue
                
                try:
                    task_id = int(args[0])
                    task = todo_core.complete_task(task_id, completed=True)
                    if task:
                        print(f"Completed task: {task.title}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please provide a valid task ID.")
            elif command == 'uncomplete':
                if len(args) < 1:
                    print("Usage: uncomplete <id>")
                    continue
                
                try:
                    task_id = int(args[0])
                    task = todo_core.complete_task(task_id, completed=False)
                    if task:
                        print(f"Marked task as incomplete: {task.title}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please provide a valid task ID.")
            elif command == 'delete':
                if len(args) < 1:
                    print("Usage: delete <id>")
                    continue
                
                try:
                    task_id = int(args[0])
                    if todo_core.delete_task(task_id):
                        print(f"Deleted task with ID {task_id}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Please provide a valid task ID.")
            elif command == 'recurring':
                if len(args) < 1:
                    print("Usage: recurring <subcommand> [args]")
                    continue
                
                subcommand = args[0].lower()
                
                if subcommand == 'add':
                    if len(args) < 3:
                        print("Usage: recurring add <task_id> <type> [days]")
                        print("  Type can be: daily, weekly, monthly")
                        print("  Days (for weekly): comma-separated days like monday,wednesday,friday")
                        continue
                    
                    try:
                        task_id = int(args[1])
                        recurrence_type = args[2]
                        
                        # Parse days if provided
                        recurrence_days = None
                        if len(args) > 3:
                            recurrence_days = [day.strip().lower() for day in args[3].split(',')]
                        
                        recurring_task = todo_core.add_recurring_task(
                            task_id=task_id,
                            recurrence_type=recurrence_type,
                            recurrence_days=recurrence_days
                        )
                        print(f"Added recurring task configuration for task {task_id}")
                    except ValueError as e:
                        print(f"Error: {e}")
                    except IndexError:
                        print("Usage: recurring add <task_id> <type> [days]")
                elif subcommand == 'list':
                    recurring_tasks = todo_core.list_recurring_tasks()
                    if not recurring_tasks:
                        print("No recurring tasks configured.")
                    else:
                        print(f"{'ID':<4} {'Task ID':<8} {'Type':<10} {'Days':<20}")
                        print("-" * 50)
                        for rt in recurring_tasks:
                            days_str = ", ".join(rt.recurrence_days) if rt.recurrence_days else ""
                            print(f"{rt.id:<4} {rt.task_id:<8} {rt.recurrence_type:<10} {days_str:<20}")
                elif subcommand == 'delete':
                    if len(args) < 2:
                        print("Usage: recurring delete <id>")
                        continue
                    
                    try:
                        recurring_id = int(args[1])
                        if todo_core.delete_recurring_task(recurring_id):
                            print(f"Deleted recurring task configuration with ID {recurring_id}")
                        else:
                            print(f"Recurring task configuration with ID {recurring_id} not found.")
                    except ValueError:
                        print("Please provide a valid recurring task configuration ID.")
                else:
                    print(f"Unknown recurring command: {subcommand}")
                    print("Available recurring commands: add, list, delete")
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    interactive_cli()