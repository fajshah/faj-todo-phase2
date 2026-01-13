# API Contracts: Phase II Todo Backend API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Complete

## Authentication Contract

All endpoints require JWT authentication via Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Responses
```json
{
  "data": { /* response data */ },
  "success": true
}
```

### Error Responses
```json
{
  "detail": "Error message",
  "success": false
}
```

## API Endpoints

### Health Check
**GET** `/health`

#### Description
Basic health check endpoint to verify backend is running

#### Authentication
Not required

#### Request
- Headers: None required
- Parameters: None
- Body: None

#### Response
- Success: 200 OK
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T12:00:00Z"
}
```

### Task Management

#### List User Tasks
**GET** `/api/tasks`

#### Description
Retrieve all tasks for the authenticated user with optional filtering

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Query Parameters:
  - `status` (optional): "pending" or "completed" to filter by completion status
- Body: None

#### Response
- Success: 200 OK
```json
{
  "data": [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    }
  ],
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

#### Create Task
**POST** `/api/tasks`

#### Description
Create a new task for the authenticated user

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Body (JSON):
```json
{
  "title": "Task title (1-200 chars)",
  "description": "Optional task description",
  "completed": false
}
```

#### Response
- Success: 201 Created
```json
{
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  },
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

- Error: 422 Validation Error
```json
{
  "detail": "Title is required and must be 1-200 characters",
  "success": false
}
```

#### Get Task
**GET** `/api/tasks/{id}`

#### Description
Retrieve a specific task for the authenticated user

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Path Parameters:
  - `id`: Task ID (integer)
- Body: None

#### Response
- Success: 200 OK
```json
{
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  },
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

- Error: 403 Forbidden
```json
{
  "detail": "Access denied - task does not belong to user",
  "success": false
}
```

- Error: 404 Not Found
```json
{
  "detail": "Task not found",
  "success": false
}
```

#### Update Task
**PUT** `/api/tasks/{id}`

#### Description
Update a specific task for the authenticated user

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Path Parameters:
  - `id`: Task ID (integer)
- Body (JSON):
```json
{
  "title": "Updated task title (1-200 chars)",
  "description": "Updated task description",
  "completed": true
}
```

#### Response
- Success: 200 OK
```json
{
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  },
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

- Error: 403 Forbidden
```json
{
  "detail": "Access denied - task does not belong to user",
  "success": false
}
```

- Error: 404 Not Found
```json
{
  "detail": "Task not found",
  "success": false
}
```

- Error: 422 Validation Error
```json
{
  "detail": "Title must be 1-200 characters",
  "success": false
}
```

#### Delete Task
**DELETE** `/api/tasks/{id}`

#### Description
Delete a specific task for the authenticated user

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Path Parameters:
  - `id`: Task ID (integer)
- Body: None

#### Response
- Success: 204 No Content
```json
{
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

- Error: 403 Forbidden
```json
{
  "detail": "Access denied - task does not belong to user",
  "success": false
}
```

- Error: 404 Not Found
```json
{
  "detail": "Task not found",
  "success": false
}
```

#### Toggle Task Completion
**PATCH** `/api/tasks/{id}/complete`

#### Description
Toggle the completion status of a specific task for the authenticated user

#### Authentication
Required - JWT token in Authorization header

#### Request
- Headers: `Authorization: Bearer <token>`
- Path Parameters:
  - `id`: Task ID (integer)
- Body (JSON):
```json
{
  "completed": true
}
```

#### Response
- Success: 200 OK
```json
{
  "data": {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z"
  },
  "success": true
}
```

- Error: 401 Unauthorized
```json
{
  "detail": "Not authenticated",
  "success": false
}
```

- Error: 403 Forbidden
```json
{
  "detail": "Access denied - task does not belong to user",
  "success": false
}
```

- Error: 404 Not Found
```json
{
  "detail": "Task not found",
  "success": false
}
```

## Error Codes

- **200 OK**: Successful request
- **201 Created**: Resource successfully created
- **204 No Content**: Successful deletion
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: User does not have permission to access resource
- **404 Not Found**: Requested resource does not exist
- **422 Validation Error**: Request data validation failed
- **500 Internal Server Error**: Unexpected server error

## Data Validation

### Task Title
- Required: Yes
- Type: String
- Length: 1-200 characters
- Pattern: Any valid text

### Task Description
- Required: No
- Type: String
- Length: No limit
- Pattern: Any valid text

### Task Completion Status
- Required: No (defaults to false)
- Type: Boolean
- Values: true or false