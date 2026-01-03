"""
Advanced Task Management Application
This application provides a menu-driven interface with advanced features.
"""
import json
from datetime import datetime, date
from enum import Enum


class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Task:
    def __init__(self, task_id, title, description="", completed=False, due_date=None, priority=Priority.MEDIUM):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.due_date = due_date  # Can be a date object or None
        self.priority = priority  # Priority enum
        self.is_recurring = False
        self.recurrence_type = None  # daily, weekly, monthly
        self.recurrence_days = None  # For weekly recurrence


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()  # Load tasks from file if they exist

    def add_task(self, title, description="", due_date=None, priority=Priority.MEDIUM):
        """Add a new task to the list."""
        task = Task(self.next_id, title, description, due_date=due_date, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()  # Save after adding
        return task

    def update_task(self, task_id, title=None, description=None):
        """Update an existing task."""
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                task.updated_at = datetime.now()
                self.save_tasks()  # Save after updating
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()  # Save after deleting
                return True
        return False

    def toggle_task_completion(self, task_id):
        """Toggle the completion status of a task."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                task.updated_at = datetime.now()
                self.save_tasks()  # Save after toggling
                return True
        return False

    def set_task_priority(self, task_id, priority):
        """Set the priority of a task."""
        for task in self.tasks:
            if task.id == task_id:
                task.priority = priority
                task.updated_at = datetime.now()
                self.save_tasks()
                return True
        return False

    def set_task_due_date(self, task_id, due_date):
        """Set the due date of a task."""
        for task in self.tasks:
            if task.id == task_id:
                task.due_date = due_date
                task.updated_at = datetime.now()
                self.save_tasks()
                return True
        return False

    def make_task_recurring(self, task_id, recurrence_type, recurrence_days=None):
        """Make a task recurring."""
        for task in self.tasks:
            if task.id == task_id:
                task.is_recurring = True
                task.recurrence_type = recurrence_type
                task.recurrence_days = recurrence_days
                task.updated_at = datetime.now()
                self.save_tasks()
                return True
        return False

    def search_tasks(self, query):
        """Search tasks by title or description."""
        query = query.lower()
        results = []
        for task in self.tasks:
            if query in task.title.lower() or query in task.description.lower():
                results.append(task)
        return results

    def filter_tasks_by_priority(self, priority):
        """Filter tasks by priority."""
        return [task for task in self.tasks if task.priority == priority]

    def filter_tasks_by_status(self, completed):
        """Filter tasks by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def filter_tasks_by_due_date(self, date):
        """Filter tasks by due date."""
        return [task for task in self.tasks if task.due_date == date]

    def save_tasks(self):
        """Save tasks to a JSON file."""
        tasks_data = []
        for task in self.tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority.value,
                'is_recurring': task.is_recurring,
                'recurrence_type': task.recurrence_type,
                'recurrence_days': task.recurrence_days
            }
            tasks_data.append(task_data)

        with open('tasks.json', 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def load_tasks(self):
        """Load tasks from a JSON file."""
        try:
            with open('tasks.json', 'r') as f:
                tasks_data = json.load(f)
                for task_data in tasks_data:
                    task = Task(
                        task_data['id'],
                        task_data['title'],
                        task_data['description'],
                        task_data['completed'],
                        date.fromisoformat(task_data['due_date']) if task_data['due_date'] else None,
                        Priority(task_data['priority'])
                    )
                    task.created_at = datetime.fromisoformat(task_data['created_at'])
                    task.updated_at = datetime.fromisoformat(task_data['updated_at'])
                    task.is_recurring = task_data.get('is_recurring', False)
                    task.recurrence_type = task_data.get('recurrence_type')
                    task.recurrence_days = task_data.get('recurrence_days')
                    self.tasks.append(task)
                    if task.id >= self.next_id:
                        self.next_id = task.id + 1
        except FileNotFoundError:
            # If file doesn't exist, start with empty task list
            pass


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("           TASK MANAGEMENT APPLICATION")
    print("="*50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Add Recurring Task")
    print("7. View Recurring Tasks")
    print("8. Set Due Date / Reminder")
    print("9. Search / Filter Tasks")
    print("10. Exit")
    print("="*50)


def get_task_input():
    """Get task details from user input."""
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty!")
        return None, None

    description = input("Enter task description (optional): ").strip()

    # Get priority
    print("Select priority:")
    print("1. Low")
    print("2. Medium")
    print("3. High")
    priority_choice = input("Enter choice (1-3, default is 2): ").strip()

    if priority_choice == "1":
        priority = Priority.LOW
    elif priority_choice == "3":
        priority = Priority.HIGH
    else:
        priority = Priority.MEDIUM  # Default to Medium

    return title, description, priority


def add_task_ui(task_manager):
    """UI for adding a task."""
    print("\n--- Add New Task ---")
    title, description, priority = get_task_input()

    if title is not None:
        task = task_manager.add_task(title, description, priority=priority)
        print(f"Task '{task.title}' added successfully with ID {task.id}!")


def view_tasks_ui(task_manager):
    """UI for viewing all tasks."""
    print("\n--- All Tasks ---")
    if not task_manager.tasks:
        print("No tasks found.")
        return

    print(f"{'ID':<3} {'Title':<20} {'Status':<12} {'Priority':<10} {'Due Date':<12} {'Recurring':<10}")
    print("-" * 80)

    for task in task_manager.tasks:
        status = "Completed" if task.completed else "Pending"
        due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
        recurring_str = "Yes" if task.is_recurring else "No"

        # Truncate title if too long
        title = task.title[:17] + "..." if len(task.title) > 20 else task.title

        print(f"{task.id:<3} {title:<20} {status:<12} {task.priority.value:<10} {due_date_str:<12} {recurring_str:<10}")


def update_task_ui(task_manager):
    """UI for updating a task."""
    print("\n--- Update Task ---")
    if not task_manager.tasks:
        print("No tasks available to update.")
        return

    view_tasks_ui(task_manager)

    try:
        task_id = int(input("\nEnter the ID of the task to update: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    # Find the task
    task = None
    for t in task_manager.tasks:
        if t.id == task_id:
            task = t
            break

    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    print(f"Current task: {task.title}")
    new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
    new_description = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()

    # Use current values if user doesn't provide new ones
    title = new_title if new_title else task.title
    description = new_description if new_description else task.description

    if task_manager.update_task(task_id, title, description):
        print("Task updated successfully!")
    else:
        print("Failed to update task.")


def delete_task_ui(task_manager):
    """UI for deleting a task."""
    print("\n--- Delete Task ---")
    if not task_manager.tasks:
        print("No tasks available to delete.")
        return

    view_tasks_ui(task_manager)

    try:
        task_id = int(input("\nEnter the ID of the task to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    if task_manager.delete_task(task_id):
        print(f"Task with ID {task_id} deleted successfully!")
    else:
        print(f"Task with ID {task_id} not found.")


def toggle_task_ui(task_manager):
    """UI for toggling task completion status."""
    print("\n--- Toggle Task Status ---")
    if not task_manager.tasks:
        print("No tasks available.")
        return

    view_tasks_ui(task_manager)

    try:
        task_id = int(input("\nEnter the ID of the task to toggle: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    if task_manager.toggle_task_completion(task_id):
        # Find the task to display its new status
        task = next((t for t in task_manager.tasks if t.id == task_id), None)
        if task:
            status = "completed" if task.completed else "incomplete"
            print(f"Task '{task.title}' marked as {status}.")
    else:
        print(f"Task with ID {task_id} not found.")


def add_recurring_task_ui(task_manager):
    """UI for making a task recurring."""
    print("\n--- Add Recurring Task ---")
    if not task_manager.tasks:
        print("No tasks available.")
        return

    view_tasks_ui(task_manager)

    try:
        task_id = int(input("\nEnter the ID of the task to make recurring: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    # Check if task exists
    task = next((t for t in task_manager.tasks if t.id == task_id), None)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    print("Select recurrence type:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")

    recurrence_choice = input("Enter choice (1-3): ").strip()

    if recurrence_choice == "1":
        recurrence_type = "daily"
        recurrence_days = None
    elif recurrence_choice == "2":
        recurrence_type = "weekly"
        days_input = input("Enter days of the week (comma-separated, e.g., monday,tuesday): ").strip()
        recurrence_days = [day.strip().lower() for day in days_input.split(',')] if days_input else None
    elif recurrence_choice == "3":
        recurrence_type = "monthly"
        recurrence_days = None
    else:
        print("Invalid choice. Task will not be made recurring.")
        return

    if task_manager.make_task_recurring(task_id, recurrence_type, recurrence_days):
        print(f"Task '{task.title}' is now recurring ({recurrence_type}).")
    else:
        print("Failed to make task recurring.")


def view_recurring_tasks_ui(task_manager):
    """UI for viewing recurring tasks."""
    print("\n--- Recurring Tasks ---")
    recurring_tasks = [task for task in task_manager.tasks if task.is_recurring]

    if not recurring_tasks:
        print("No recurring tasks found.")
        return

    print(f"{'ID':<3} {'Title':<20} {'Type':<10} {'Days':<20}")
    print("-" * 50)

    for task in recurring_tasks:
        days_str = ", ".join(task.recurrence_days) if task.recurrence_days else "N/A"
        title = task.title[:17] + "..." if len(task.title) > 20 else task.title
        print(f"{task.id:<3} {title:<20} {task.recurrence_type:<10} {days_str:<20}")


def set_due_date_ui(task_manager):
    """UI for setting due date/reminder."""
    print("\n--- Set Due Date / Reminder ---")
    if not task_manager.tasks:
        print("No tasks available.")
        return

    view_tasks_ui(task_manager)

    try:
        task_id = int(input("\nEnter the ID of the task: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return

    # Check if task exists
    task = next((t for t in task_manager.tasks if t.id == task_id), None)
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    due_date_input = input("Enter due date (YYYY-MM-DD format): ").strip()

    try:
        due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
        if task_manager.set_task_due_date(task_id, due_date):
            print(f"Due date set for task '{task.title}' to {due_date}.")
        else:
            print("Failed to set due date.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")


def search_filter_tasks_ui(task_manager):
    """UI for searching and filtering tasks."""
    print("\n--- Search / Filter Tasks ---")
    print("1. Search by keyword")
    print("2. Filter by priority")
    print("3. Filter by status")
    print("4. Filter by due date")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        query = input("Enter search query: ").strip()
        results = task_manager.search_tasks(query)

        if results:
            print(f"\nSearch results for '{query}':")
            print(f"{'ID':<3} {'Title':<20} {'Status':<12} {'Priority':<10} {'Due Date':<12}")
            print("-" * 60)

            for task in results:
                status = "Completed" if task.completed else "Pending"
                due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
                title = task.title[:17] + "..." if len(task.title) > 20 else task.title
                print(f"{task.id:<3} {title:<20} {status:<12} {task.priority.value:<10} {due_date_str:<12}")
        else:
            print(f"No tasks found matching '{query}'.")

    elif choice == "2":
        print("Select priority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")

        priority_choice = input("Enter choice (1-3): ").strip()

        if priority_choice == "1":
            priority = Priority.LOW
        elif priority_choice == "2":
            priority = Priority.MEDIUM
        elif priority_choice == "3":
            priority = Priority.HIGH
        else:
            print("Invalid choice.")
            return

        results = task_manager.filter_tasks_by_priority(priority)

        if results:
            print(f"\nTasks with {priority.value} priority:")
            print(f"{'ID':<3} {'Title':<20} {'Status':<12} {'Due Date':<12}")
            print("-" * 50)

            for task in results:
                status = "Completed" if task.completed else "Pending"
                due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
                title = task.title[:17] + "..." if len(task.title) > 20 else task.title
                print(f"{task.id:<3} {title:<20} {status:<12} {due_date_str:<12}")
        else:
            print(f"No tasks with {priority.value} priority found.")

    elif choice == "3":
        print("Select status:")
        print("1. Completed")
        print("2. Pending")

        status_choice = input("Enter choice (1-2): ").strip()

        if status_choice == "1":
            completed = True
        elif status_choice == "2":
            completed = False
        else:
            print("Invalid choice.")
            return

        results = task_manager.filter_tasks_by_status(completed)

        if results:
            status_str = "Completed" if completed else "Pending"
            print(f"\n{status_str} tasks:")
            print(f"{'ID':<3} {'Title':<20} {'Priority':<10} {'Due Date':<12}")
            print("-" * 50)

            for task in results:
                due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
                title = task.title[:17] + "..." if len(task.title) > 20 else task.title
                print(f"{task.id:<3} {title:<20} {task.priority.value:<10} {due_date_str:<12}")
        else:
            print(f"No {status_str.lower()} tasks found.")

    elif choice == "4":
        due_date_input = input("Enter due date to filter (YYYY-MM-DD format): ").strip()

        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
            results = task_manager.filter_tasks_by_due_date(due_date)

            if results:
                print(f"\nTasks due on {due_date}:")
                print(f"{'ID':<3} {'Title':<20} {'Status':<12} {'Priority':<10}")
                print("-" * 50)

                for task in results:
                    status = "Completed" if task.completed else "Pending"
                    title = task.title[:17] + "..." if len(task.title) > 20 else task.title
                    print(f"{task.id:<3} {title:<20} {status:<12} {task.priority.value:<10}")
            else:
                print(f"No tasks due on {due_date}.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")

    else:
        print("Invalid choice.")


def main():
    """Main application loop."""
    print("Welcome to the Advanced Task Management Application!")

    # Initialize the task manager
    task_manager = TaskManager()

    # Main menu loop
    while True:
        display_menu()

        choice = input("\nEnter your choice (1-10): ").strip()

        if choice == "1":
            add_task_ui(task_manager)
        elif choice == "2":
            view_tasks_ui(task_manager)
        elif choice == "3":
            update_task_ui(task_manager)
        elif choice == "4":
            delete_task_ui(task_manager)
        elif choice == "5":
            toggle_task_ui(task_manager)
        elif choice == "6":
            add_recurring_task_ui(task_manager)
        elif choice == "7":
            view_recurring_tasks_ui(task_manager)
        elif choice == "8":
            set_due_date_ui(task_manager)
        elif choice == "9":
            search_filter_tasks_ui(task_manager)
        elif choice == "10":
            print("\nThank you for using the Task Management Application!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 10.")

        # Pause to let user see the result before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()