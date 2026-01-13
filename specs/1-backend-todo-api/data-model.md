# Data Model: Phase II Todo Backend API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-08
**Status**: Complete

## Entity: Task

### Fields
- **id** (Integer, Primary Key, Auto-generated)
  - Purpose: Unique identifier for each task
  - Constraints: Auto-incrementing integer, required
  - Validation: System-generated, not user-provided

- **user_id** (String, Required)
  - Purpose: Links task to the authenticated user
  - Constraints: Comes from JWT token subject claim, required
  - Validation: Must match authenticated user's ID from JWT
  - Index: Indexed for efficient user-based queries

- **title** (String, Required)
  - Purpose: Brief description of the task
  - Constraints: 1-200 characters, required
  - Validation: Length between 1 and 200 characters
  - Example: "Complete project proposal", "Buy groceries"

- **description** (Text, Optional)
  - Purpose: Detailed information about the task
  - Constraints: Optional, can be null/empty
  - Validation: No specific length limits
  - Example: "Write a comprehensive proposal document for the new client project"

- **completed** (Boolean, Default: False)
  - Purpose: Tracks completion status of the task
  - Constraints: Boolean value, defaults to False
  - Validation: Must be true or false
  - Example: false (pending), true (completed)

- **created_at** (DateTime, Auto-generated)
  - Purpose: Timestamp when task was created
  - Constraints: Auto-generated on creation, required
  - Validation: System-generated timestamp
  - Format: ISO 8601 format

- **updated_at** (DateTime, Auto-generated)
  - Purpose: Timestamp when task was last modified
  - Constraints: Auto-generated on creation and updates, required
  - Validation: System-generated timestamp, updates on any modification
  - Format: ISO 8601 format

### Relationships
- **User Relationship**: Tasks are associated with users through user_id field
  - Each task belongs to exactly one user
  - Users can have multiple tasks
  - Implemented via user_id field that matches JWT token subject

### Constraints
- **User Isolation**: All queries must filter by user_id to ensure data isolation
- **Title Length**: Title must be between 1 and 200 characters
- **Required Fields**: id, user_id, title, created_at, updated_at are required
- **Default Values**: completed defaults to False, timestamps auto-generated

### Indexes
- **Primary Index**: id (auto-created)
- **User Query Index**: user_id (for efficient user-based queries)
- **Status Query Index**: completed (for filtering by completion status)

## Entity: User (Implicit via JWT)

### Fields (derived from JWT)
- **user_id** (String, from JWT "sub" claim)
  - Purpose: Unique identifier for authenticated user
  - Source: JWT token subject claim
  - Validation: Verified through JWT signature and expiration check
  - Not stored in database but used for user_id field in Task entity

### Relationships
- **Task Ownership**: User identified by JWT owns tasks with matching user_id
- **Data Isolation**: User can only access tasks where user_id matches their JWT subject

## Validation Rules

### Task Creation
- Title must be provided (1-200 characters)
- Description is optional
- Completed defaults to false
- user_id is automatically set from authenticated user's JWT

### Task Updates
- Title must remain 1-200 characters if changed
- Only the task owner can update their tasks
- updated_at timestamp automatically updated

### Task Deletion
- Only the task owner can delete their tasks
- Task must exist to be deleted

## State Transitions

### Task Completion
- Initial state: completed = false
- Transition: PUT/PATCH request to toggle completion status
- Final state: completed = true

### Task Modification
- Initial state: Task exists with specific title/description
- Transition: PUT request with new values
- Final state: Task updated with new values and updated timestamp

## Data Access Patterns

### User-Specific Queries
- Query all tasks for a specific user using user_id filter
- Query completed/incomplete tasks for a user
- Query specific task by ID with user ownership verification

### Security Patterns
- All queries must include user_id filter
- No direct access to tasks without user authentication
- User isolation enforced at the application level