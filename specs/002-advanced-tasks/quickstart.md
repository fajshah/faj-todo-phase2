# Quickstart Guide: Advanced Task Management Features

## Prerequisites

- Python 3.13+
- PostgreSQL database
- Redis server (for background job processing)
- Node.js and npm (for frontend development)

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd my-todo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync  # or pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb todo_app

# Run database migrations
python -m src.database.migrate
```

### 3. Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost/todo_app
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
WEB_PUSH_PRIVATE_KEY=your-web-push-private-key
WEB_PUSH_PUBLIC_KEY=your-web-push-public-key
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Backend

```bash
# Terminal 1: Start the web server
python -m src.main

# Terminal 2: Start the background job processor
celery -A src.background.worker worker --loglevel=info
```

### Frontend

```bash
# In the frontend directory
npm start
```

## Key Components

### 1. Recurring Task Service

The recurring task service handles the creation of new task instances when a recurring task is completed:

```python
from src.services.recurring_task_service import RecurringTaskService

service = RecurringTaskService()
# When a recurring task is marked as complete:
next_task = service.create_next_task_instance(task_id)
```

### 2. Reminder Service

The reminder service schedules and sends notifications:

```python
from src.services.reminder_service import ReminderService

service = ReminderService()
# Schedule a reminder for a task:
service.schedule_reminder(task_id, reminder_time)
```

### 3. Data Models

Key data models are defined in `src/models/`:

- `Task`: Base task model
- `RecurringTask`: Recurrence configuration
- `TaskReminder`: Scheduled reminders
- `TaskInstance`: Individual instances of recurring tasks

## API Endpoints

### Task Management
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task (with optional recurrence and reminder)
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `POST /api/tasks/{id}/complete` - Mark task as complete

### Recurring Tasks
- `POST /api/recurring-tasks` - Create a recurring task configuration
- `PUT /api/recurring-tasks/{id}` - Update recurrence configuration
- `DELETE /api/recurring-tasks/{id}` - Disable recurrence

### Reminders
- `POST /api/reminders` - Schedule a reminder for a task
- `GET /api/reminders/upcoming` - Get upcoming reminders
- `PUT /api/reminders/{id}/sent` - Mark reminder as sent

## Background Jobs

The system uses Celery for background job processing:

1. **Reminder Scheduler**: Runs periodically to check for upcoming reminders
2. **Recurring Task Handler**: Processes completed recurring tasks and creates new instances

## Testing

Run the test suite:

```bash
# Backend tests
pytest tests/

# Frontend tests
cd frontend && npm test
```

## Deployment

For production deployment:

1. Set up PostgreSQL and Redis in production
2. Configure environment variables
3. Deploy backend application
4. Deploy frontend application
5. Start background job processors
6. Set up reverse proxy (e.g., Nginx)