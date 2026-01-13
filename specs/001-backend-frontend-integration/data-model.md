# Data Model: Backend-Frontend Integration

## Entities

### User
- **Fields**:
  - id: UUID (primary key)
  - email: String (unique, required)
  - password_hash: String (required, hashed)
  - created_at: DateTime (auto-generated)
  - updated_at: DateTime (auto-generated)
- **Validation**:
  - Email must be valid email format
  - Password must be 8+ characters with mixed case
  - Email must be unique across all users
- **Relationships**:
  - One-to-many with Task (via user_id foreign key)

### Task
- **Fields**:
  - id: UUID (primary key)
  - title: String (required)
  - description: Text (optional)
  - completed: Boolean (default: False)
  - priority: String (values: "High", "Medium", "Low", default: "Medium")
  - user_id: UUID (foreign key to User)
  - created_at: DateTime (auto-generated)
  - updated_at: DateTime (auto-generated)
- **Validation**:
  - Title must be 1-200 characters
  - Priority must be one of "High", "Medium", "Low"
  - Task must belong to a valid user
- **Relationships**:
  - Many-to-one with User (via user_id foreign key)

## State Transitions

### Task State Transitions
- Created → Active (initial state when created)
- Active → Completed (when marked complete)
- Completed → Active (when unmarked complete)

## Constraints
- All tasks must be associated with a valid user
- Users cannot access tasks belonging to other users
- Task titles must not be empty
- Passwords must meet security requirements (8+ chars, mixed case)