# Feature Specification: Phase II Todo Backend API

**Feature Branch**: `1-backend-todo-api`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Scope: BACKEND ONLY — FULL IMPLEMENTATION & FRONTEND INTEGRATION

Create a complete, production-grade backend specification for the Phase II
Todo Full-Stack Web Application using FastAPI, SQLModel, and Neon Serverless
PostgreSQL.

This backend must integrate seamlessly with an already completed Next.js
frontend and strictly follow the approved Phase II Constitution.

-----------------------------------
CONTEXT
-----------------------------------

Frontend Status:
- Frontend is fully complete and running on http://localhost:3000
- Uses JWT tokens issued by Better Auth
- All API calls include Authorization: Bearer <token> header

Backend s.py (task CRUD routes)
  - health.py (optional health check)

-----------------------------------
DATABASE SPECIFICATION (SQLModel)
-----------------------------------

Define SQLModel models and schema:

Task Model:
- id: integer (primary key)
- user_id: string (from JWT subject)
- title: string (required, 1–200 chars)
- description: text (optional)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

Constraints:
- All queries MUST filter by user_id
- user_id comes ONLY from verified JWT
- Database connection must use NEON_DATABASE_URL

-----------------------------------
AUTHENTICATION & SECURITY
-----------------------------------

JWT Verification:
- Extract token from Authorization header
- Verify JWT signature using BETTER_AUTH_SECRET
- Validate token expiration
- Decode user_id from token payload
- Reject invalid or missing tokens with 401

Rules:
- Backend must NEVER trust user_id from request body or params
- JWT user_id is the single source of truth
- Token verification middleware or dependency REQUIRED

-----------------------------------
API ENDPOINT SPECIFICATION
-----------------------------------

All endpoints are prefixed with /api

GET /api/tasks
- List all tasks for authenticated user
- Optional filters: status (pending/completed)
- Return only user's tasks

POST /api/tasks
- Create a new task
- Associate task with authenticated user

GET /api/tasks/{id}
- Fetch a single task
- Verify task ownership

PUT /api/tasks/{id}
- Update title, description, completed status
- Verify task ownership

DELETE /api/tasks/{id}
- Delete task
- Verify task ownership

PATCH /api/tasks/{id}/complete
- Toggle completed state
- Verify task ownership

-----------------------------------
ERROR HANDLING
-----------------------------------

Define standard error responses:
- 401 Unauthorized (missing/invalid token)
- 403 Forbidden (accessing another user's task)
- 404 Not Found (task does not exist)
- 422 Validation Error (invalid input)
- 500 Internal Server Error (unexpected)

Errors must be JSON and frontend-friendly.

-----------------------------------
FRONTEND INTEGRATION CONTRACT
-----------------------------------

The backend must support:
- CORS for http://localhost:3000
- Authorization header with Bearer token
- JSON request/response only
- Stable response shapes

No frontend changes should be required.

-----------------------------------
NON-FUNCTIONAL REQUIREMENTS
-----------------------------------

- Clean, readable, maintainable code
- Explicit logic (no magic or shortcuts)
- Proper separation of concerns
- Async-compatible FastAPI patterns
- Production-grade practices

-----------------------------------
OUT OF SCOPE
-----------------------------------

- Frontend UI
- Better Auth implementation itself
- Database migrations tooling
- AI or chatbot features

-----------------------------------
OUTPUT REQUIREMENTS
-----------------------------------

- One complete Markdown specification
- Clear sections and headings
- No code generation
- No questions
- No explanations
- No agents or skills
- Ready for /sp.plan execution"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Tasks (Priority: P1)

Authenticated users need to create new tasks in their personal task list. The user logs into the Next.js frontend, navigates to the task creation interface, fills in task details (title, optional description), and submits the form. The frontend sends a POST request to the backend API with proper authentication token, and the new task appears in their task list.

**Why this priority**: Creating tasks is the core functionality of a todo application - without this capability, users cannot use the application for its primary purpose.

**Independent Test**: Can be fully tested by creating a single task through the API and verifying it's stored in the database and returned when fetching the user's tasks, delivering the core value of task creation.

**Acceptance Scenarios**:

1. **Given** user is authenticated with valid JWT token, **When** user submits task creation request with valid title, **Then** new task is created for that user and returned in the response
2. **Given** user is authenticated with valid JWT token, **When** user submits task creation request with title and description, **Then** new task with both title and description is created for that user
3. **Given** user is not authenticated or has invalid token, **When** user attempts to create a task, **Then** API returns 401 Unauthorized error

---

### User Story 2 - View Personal Task List (Priority: P1)

Authenticated users need to view their personal task list. The user logs into the Next.js frontend and navigates to their dashboard, where they see a list of all their tasks. The frontend fetches the user's tasks from the backend API using their authentication token, and displays them in an organized manner.

**Why this priority**: Viewing tasks is essential for users to manage and track their work - without this capability, users cannot see what they've created.

**Independent Test**: Can be fully tested by creating multiple tasks for a user and verifying they can retrieve only their own tasks through the API, delivering the core value of task visibility.

**Acceptance Scenarios**:

1. **Given** user has multiple tasks in their account, **When** user requests their task list, **Then** API returns only tasks belonging to that user
2. **Given** user has no tasks in their account, **When** user requests their task list, **Then** API returns empty list with success status
3. **Given** user is not authenticated or has invalid token, **When** user attempts to fetch tasks, **Then** API returns 401 Unauthorized error

---

### User Story 3 - Update and Complete Tasks (Priority: P2)

Authenticated users need to update their task details and mark tasks as completed. The user navigates to their task list, selects a task to edit, modifies its details (title, description) or toggles its completion status, and saves the changes. The frontend sends update requests to the backend API with proper authentication.

**Why this priority**: Task management requires the ability to modify existing tasks and track completion status, which is crucial for productivity.

**Independent Test**: Can be fully tested by updating a user's task through the API and verifying the changes are persisted and reflected when fetching the task again, delivering the value of task modification.

**Acceptance Scenarios**:

1. **Given** user owns a task, **When** user updates task title and description, **Then** task is updated with new values and returned in response
2. **Given** user owns a task, **When** user toggles task completion status, **Then** task completion status is updated and returned in response
3. **Given** user attempts to update another user's task, **When** user sends update request, **Then** API returns 403 Forbidden error

---

### User Story 4 - Delete Tasks (Priority: P2)

Authenticated users need to remove tasks they no longer need. The user navigates to their task list, selects a task they want to remove, and triggers the delete action. The frontend sends a delete request to the backend API with proper authentication, and the task is removed from their list.

**Why this priority**: Task management includes the ability to remove completed or irrelevant tasks, which helps maintain a clean task list.

**Independent Test**: Can be fully tested by deleting a user's task through the API and verifying it no longer appears in their task list, delivering the value of task cleanup.

**Acceptance Scenarios**:

1. **Given** user owns a task, **When** user sends delete request for that task, **Then** task is removed from database and API returns success response
2. **Given** user attempts to delete another user's task, **When** user sends delete request, **Then** API returns 403 Forbidden error
3. **Given** user attempts to delete a non-existent task, **When** user sends delete request, **Then** API returns 404 Not Found error

---

### Edge Cases

- What happens when a user tries to access another user's tasks?
- How does the system handle expired JWT tokens?
- What happens when a user tries to create a task with an empty title?
- How does the system handle extremely long task titles or descriptions?
- What happens when the database is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens from Authorization header using BETTER_AUTH_SECRET
- **FR-002**: System MUST extract user_id from verified JWT token payload and use it as the single source of truth for user identification
- **FR-003**: System MUST filter all database queries by user_id to ensure data isolation between users
- **FR-004**: System MUST support CRUD operations for tasks (Create, Read, Update, Delete)
- **FR-005**: System MUST provide endpoint to toggle task completion status
- **FR-006**: System MUST enforce task title length between 1-200 characters
- **FR-007**: System MUST store task details including title, description, completion status, and timestamps
- **FR-008**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404, 422, 500)
- **FR-009**: System MUST support optional filtering of tasks by completion status
- **FR-010**: System MUST implement CORS to allow requests from http://localhost:3000
- **FR-011**: System MUST return JSON responses for all API endpoints
- **FR-012**: System MUST validate input data and return 422 for invalid inputs
- **FR-013**: System MUST reject requests without valid Authorization header with 401 status

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with properties (id, user_id, title, description, completed status, creation timestamp, update timestamp)
- **User**: Represents an authenticated user identified by user_id from JWT token
- **JWT Token**: Authentication mechanism that provides user identity and access verification

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks through the frontend with 99% success rate
- **SC-002**: Users can retrieve their personal task list within 2 seconds response time
- **SC-003**: Users can update and delete their tasks with 99% success rate
- **SC-004**: System prevents unauthorized access to other users' tasks with 100% accuracy
- **SC-005**: API endpoints return appropriate error responses for invalid requests
- **SC-006**: Frontend can successfully integrate with backend API without requiring frontend code changes
- **SC-007**: System handles 100 concurrent users creating and managing tasks without performance degradation
- **SC-008**: All API requests from frontend to backend complete successfully with proper authentication