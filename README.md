# Advanced Task Management Application

This is a comprehensive task management application with support for recurring tasks and time-based reminders.

## Architecture

The application is built with a clean architecture that separates concerns:

- **Core Logic** (`src/core/`): Shared business logic between web API and CLI
- **Web API** (`src/main.py`): FastAPI-based web interface
- **CLI** (`src/cli.py`): Command-line interface using Typer
- **Services** (`src/services/`): Business service implementations
- **API Routers** (`src/api/`): API endpoint definitions
- **Models** (`src/models/`): Database models
- **Background Jobs** (`src/background/`): Scheduled tasks and reminders

## Running the Application

### Web API

To run the web API:

```bash
# Using the module approach
python -m src.main

# Or using uvicorn directly
uvicorn src.main:app --reload
```

The API will be available at `http://0.0.0.0:8000`

### Command Line Interface (CLI)

To run the CLI application:

```bash
# Using the module approach
python -m src.cli

# Or using the installed script
todo-cli
```

## CLI Commands

The CLI provides a comprehensive set of commands for managing tasks:

### Basic Task Management

- **Add a task**:
  ```bash
  todo-cli add "My new task" --desc "Description of the task" --due-date 2023-12-31 --priority high
  ```

- **List tasks**:
  ```bash
  todo-cli list
  # Show all tasks including completed ones
  todo-cli list --all
  # Show only recurring tasks
  todo-cli list --recurring
  ```

- **Complete a task**:
  ```bash
  todo-cli complete 1
  ```

- **Mark a task as incomplete**:
  ```bash
  todo-cli uncomplete 1
  ```

- **Delete a task**:
  ```bash
  todo-cli delete 1
  ```

### Recurring Tasks

- **Make a task recurring**:
  ```bash
  todo-cli recurring add 1 --type weekly --days monday,wednesday,friday
  ```

- **List recurring tasks**:
  ```bash
  todo-cli recurring list
  ```

- **Delete a recurring task configuration**:
  ```bash
  todo-cli recurring delete 1
  ```

## Design Decisions

1. **Shared Core Logic**: The `src/core/` module contains all business logic that is shared between the web API and CLI, preventing code duplication.

2. **Clean Separation**: The CLI and web API are separate entry points but use the same underlying business logic.

3. **Type Safety**: Using dataclasses and enums for type safety and better IDE support.

4. **Error Handling**: Proper error handling with meaningful error messages.

5. **CLI Framework**: Using Typer for a professional CLI experience with automatic help generation and validation.

## Project Structure

```
src/
├── core/              # Shared business logic
│   └── todo_core.py   # Core business logic
├── models/            # Database models
├── services/          # Business services
├── api/               # API routers
├── cli.py             # CLI entry point
├── main.py            # Web API entry point
└── database.py        # Database configuration
```

## Running Tests

```bash
pytest
```

## Dependencies

- FastAPI: Web framework
- Typer: CLI framework
- SQLAlchemy: Database ORM
- Celery: Background job processing
- Redis: Task queue
- Pydantic: Data validation