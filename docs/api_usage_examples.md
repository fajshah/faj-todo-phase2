# API Usage Examples for Phase II Todo Backend API

This document provides practical examples for using the API endpoints of the Phase II Todo Backend API.

## Authentication

All endpoints (except health check) require JWT authentication via the Authorization header:

```
Authorization: Bearer <jwt_token>
```

The JWT tokens are expected to be issued by Better Auth and must contain the user ID in the "sub" claim.

## Health Check

### GET /health

Check if the API is running properly.

```bash
curl -X GET http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T12:00:00Z"
}
```

## Task Management

### GET /api/v1/tasks

Get all tasks for the authenticated user with optional status filtering.

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "data": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "user_id": "user123",
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    }
  ],
  "success": true
}
```

### POST /api/v1/tasks

Create a new task for the authenticated user.

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Task description",
    "completed": false
  }'
```

Response:
```json
{
  "data": {
    "id": 1,
    "title": "New Task",
    "description": "Task description",
    "completed": false,
    "user_id": "user123",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  },
  "success": true
}
```

### GET /api/v1/tasks/{id}

Get a specific task for the authenticated user.

```bash
curl -X GET http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "data": {
    "id": 1,
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "user_id": "user123",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  },
  "success": true
}
```

### PUT /api/v1/tasks/{id}

Update a specific task for the authenticated user.

```bash
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true
  }'
```

Response:
```json
{
  "data": {
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true,
    "user_id": "user123",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  },
  "success": true
}
```

### DELETE /api/v1/tasks/{id}

Delete a specific task for the authenticated user.

```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "success": true
}
```

### PATCH /api/v1/tasks/{id}/complete

Toggle the completion status of a specific task for the authenticated user.

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

Response:
```json
{
  "data": {
    "id": 1,
    "title": "Sample task",
    "description": "Task description",
    "completed": true,
    "user_id": "user123",
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  },
  "success": true
}
```

## Error Responses

The API returns consistent error responses in the following format:

```json
{
  "detail": "Error message",
  "success": false
}
```

### Common Error Codes

- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: User does not have permission to access resource
- **404 Not Found**: Requested resource does not exist
- **422 Validation Error**: Request data validation failed
- **500 Internal Server Error**: Unexpected server error