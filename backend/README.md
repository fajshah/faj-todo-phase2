# Todo Backend API

Backend API for the Phase II Todo Full-Stack Web Application built with Python FastAPI.

## Features

- RESTful API with authentication
- Task management (CRUD operations)
- User authentication and authorization
- Database integration with SQLModel and SQLite
- CORS support for frontend integration

## Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Tasks
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle task completion

### Health
- `GET /health` - Health check
- `GET /health/database` - Database health check

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the server:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Environment Variables

- `NEON_DATABASE_URL` - Database connection URL
- `BETTER_AUTH_SECRET` - Secret key for JWT authentication
- `FRONTEND_URL` - Frontend origin URL for CORS
- `CORS_ALLOW_ORIGINS` - Additional allowed origins (comma-separated)