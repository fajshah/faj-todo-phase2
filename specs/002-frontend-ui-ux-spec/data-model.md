# Frontend Data Model: Todo Application

**Feature**: Frontend UI/UX Specification
**Date**: 2026-01-06
**Status**: Design

## Entity: Task

**Description**: Represents a user's todo item that will be displayed and managed in the UI

**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - The main title/description of the task
- `description`: string (optional) - Detailed description of the task
- `completed`: boolean - Whether the task has been completed
- `createdAt`: string (ISO date) - When the task was created
- `updatedAt`: string (ISO date) - When the task was last modified
- `dueDate`: string (ISO date, optional) - When the task is due

**Validation Rules**:
- `title` must be 1-255 characters
- `description` can be up to 1000 characters if provided
- `completed` defaults to false
- `createdAt` and `updatedAt` are automatically managed by the system

**State Transitions**:
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

## Entity: User Session

**Description**: Represents the authenticated state of a user in the frontend UI

**Fields**:
- `token`: string - JWT token for API authentication
- `userId`: string - Unique identifier of the authenticated user
- `expiresAt`: string (ISO date) - When the token expires
- `isLoggedIn`: boolean - Whether the user is currently logged in

**Validation Rules**:
- `token` must be a valid JWT format
- `expiresAt` must be in the future
- `isLoggedIn` is derived from token validity

**State Transitions**:
- `loggedOut` → `loggedIn`: When user successfully authenticates
- `loggedIn` → `loggedOut`: When user logs out or token expires

## Entity: UI State

**Description**: Represents various UI states that affect the user interface

**Fields**:
- `loading`: boolean - Whether the UI is in a loading state
- `error`: string (optional) - Error message if in error state
- `success`: string (optional) - Success message for user feedback
- `currentView`: string - Current page/view being displayed

**Validation Rules**:
- Only one of `error` or `success` should be active at a time
- `currentView` must be a valid route in the application

## Entity: Form State

**Description**: Represents the state of forms in the application

**Fields**:
- `values`: object - Current values in the form fields
- `errors`: object - Validation errors for each field
- `touched`: object - Which fields have been interacted with
- `isSubmitting`: boolean - Whether the form is currently being submitted

**Validation Rules**:
- `errors` keys must match `values` keys
- `touched` keys must match `values` keys
- `isSubmitting` should be false when not actively submitting

## Entity: Filter State

**Description**: Represents the current filtering and sorting state of task lists

**Fields**:
- `showCompleted`: boolean - Whether to show completed tasks
- `sortBy`: string - How to sort tasks (e.g., 'createdAt', 'dueDate', 'title')
- `sortDirection`: string - Direction to sort ('asc' or 'desc')
- `searchQuery`: string (optional) - Text to search for in task titles/descriptions

**Validation Rules**:
- `sortBy` must be one of the allowed values
- `sortDirection` must be 'asc' or 'desc'
- `searchQuery` can be empty but not null