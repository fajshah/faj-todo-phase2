# Data Model: Advanced Task Management Features

## Entities

### Task
Represents a single task in the system.

**Fields:**
- `id` (UUID/Integer): Unique identifier for the task
- `title` (String): Title of the task
- `description` (Text): Detailed description of the task
- `completed` (Boolean): Whether the task is completed
- `created_at` (DateTime): Timestamp when the task was created
- `updated_at` (DateTime): Timestamp when the task was last updated
- `due_date` (Date, nullable): Date when the task is due
- `due_time` (Time, nullable): Time when the task is due
- `priority` (Enum): Priority level (low, medium, high)
- `is_recurring` (Boolean): Whether this task is recurring
- `user_id` (UUID/Integer): Reference to the user who owns the task

**Relationships:**
- One-to-many with TaskReminder (one task can have multiple reminders)
- One-to-many with RecurringTask (one task can have one recurrence configuration)

**Validation Rules:**
- Title is required and must be between 1-255 characters
- Priority must be one of the allowed values
- If due_date is set, it must be a valid future date
- If due_time is set, due_date must also be set

### RecurringTask
Represents the recurrence configuration for a recurring task.

**Fields:**
- `id` (UUID/Integer): Unique identifier for the recurrence configuration
- `task_id` (UUID/Integer): Reference to the original task
- `recurrence_type` (Enum): Type of recurrence (daily, weekly, monthly)
- `recurrence_days` (JSON/Array, nullable): Days of the week for weekly recurrence (e.g., ["monday", "wednesday", "friday"])
- `next_due_date` (Date): The next date when this task is due
- `end_date` (Date, nullable): Date when recurrence should end (optional)
- `max_occurrences` (Integer, nullable): Maximum number of occurrences (optional)
- `created_at` (DateTime): Timestamp when the recurrence was created
- `updated_at` (DateTime): Timestamp when the recurrence was last updated

**Relationships:**
- Many-to-one with Task (many recurring tasks link to one base task)
- One-to-many with TaskInstance (recurring task generates multiple instances)

**Validation Rules:**
- recurrence_type must be one of the allowed values
- If recurrence_type is "weekly", recurrence_days must contain valid day names
- next_due_date must be a valid future date
- end_date must be after the current date if specified
- max_occurrences must be a positive integer if specified

### TaskReminder
Represents a scheduled reminder for a task.

**Fields:**
- `id` (UUID/Integer): Unique identifier for the reminder
- `task_id` (UUID/Integer): Reference to the task
- `reminder_time` (DateTime): When the reminder should be sent
- `sent` (Boolean): Whether the reminder has been sent
- `sent_at` (DateTime, nullable): When the reminder was actually sent
- `notification_type` (Enum): Type of notification (browser, email, etc.)
- `created_at` (DateTime): Timestamp when the reminder was created

**Relationships:**
- Many-to-one with Task (many reminders can be associated with one task)

**Validation Rules:**
- reminder_time must be before the task's due_time
- notification_type must be one of the allowed values
- A task cannot have duplicate reminder times

### TaskInstance
Represents a specific occurrence of a recurring task.

**Fields:**
- `id` (UUID/Integer): Unique identifier for the instance
- `original_task_id` (UUID/Integer): Reference to the original recurring task
- `instance_due_date` (Date): Due date for this specific instance
- `instance_due_time` (Time, nullable): Due time for this specific instance
- `completed` (Boolean): Whether this instance is completed
- `created_at` (DateTime): Timestamp when the instance was created
- `completed_at` (DateTime, nullable): When this instance was completed

**Relationships:**
- Many-to-one with RecurringTask (many instances generated from one recurring task)

**Validation Rules:**
- instance_due_date must be a valid date
- completed_at can only be set if completed is true

### User
Represents a user in the system.

**Fields:**
- `id` (UUID/Integer): Unique identifier for the user
- `username` (String): User's username
- `email` (String): User's email address
- `timezone` (String): User's preferred timezone (e.g., "America/New_York")
- `created_at` (DateTime): Timestamp when the user was created
- `updated_at` (DateTime): Timestamp when the user was last updated

**Relationships:**
- One-to-many with Task (one user can have many tasks)
- One-to-many with RecurringTask (one user can have many recurring tasks)

**Validation Rules:**
- Username is required and must be unique
- Email is required, must be valid, and must be unique
- Timezone must be a valid IANA timezone identifier

## State Transitions

### Task States
- `incomplete` → `complete` (when user marks task as done)
- `complete` → `incomplete` (when user unmarks task as done)

### RecurringTask States
- `active` (when recurrence is ongoing)
- `ended` (when end_date is reached or max_occurrences is met)

### TaskReminder States
- `scheduled` → `sent` (when reminder is delivered)
- `sent` (final state)

## Indexes

### Task Table
- Index on `user_id` for efficient user-specific queries
- Index on `due_date` for efficient due date queries
- Index on `completed` for filtering completed/incomplete tasks

### RecurringTask Table
- Index on `task_id` for efficient lookup of recurrence configuration
- Index on `next_due_date` for efficient scheduling queries

### TaskReminder Table
- Index on `task_id` for efficient lookup of reminders for a task
- Index on `reminder_time` for efficient scheduling queries
- Index on `sent` for filtering unsent reminders

### TaskInstance Table
- Index on `original_task_id` for efficient lookup of instances for a recurring task
- Index on `instance_due_date` for efficient due date queries
- Index on `completed` for filtering completed/incomplete instances