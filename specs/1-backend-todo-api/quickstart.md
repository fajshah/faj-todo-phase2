# Quickstart Guide: Phase II Todo Backend API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Complete

## Overview
This guide provides setup instructions for the Phase II Todo Backend API built with FastAPI, SQLModel, and Neon PostgreSQL.

## Prerequisites
- Python 3.9 or higher
- Neon PostgreSQL database instance
- Better Auth secret key for JWT verification
- Node.js and npm (for frontend integration testing)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
NEON_DATABASE_URL=your_neon_database_url_here
BETTER_AUTH_SECRET=your_better_auth_secret_here
```

### 5. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health` - Verify the API is running

### Task Management
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## Testing with Frontend
The backend is configured to allow requests from `http://localhost:3000` (Next.js frontend).

## Environment Variables
- `NEON_DATABASE_URL`: Connection string for Neon PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for verifying Better Auth JWT tokens
- `DEBUG`: Set to "True" for development (optional)

## Common Issues

### Database Connection Issues
- Verify NEON_DATABASE_URL is correctly formatted
- Ensure Neon database is active and accessible

### JWT Authentication Issues
- Confirm BETTER_AUTH_SECRET matches Better Auth configuration
- Verify JWT tokens are properly formatted with Authorization header

### CORS Issues
- Ensure frontend is running on http://localhost:3000
- Check that Authorization header is being sent with requests