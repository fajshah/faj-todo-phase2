# Implementation Plan: Phase II Todo Backend ↔ Frontend Integration

**Feature**: full-backend-frontend-integration
**Created**: 2026-01-09
**Status**: Draft
**Plan**: Complete integration between frontend and backend

## Technical Context

### Known Parameters
- **Frontend Stack**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend Stack**: FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
- **Authentication**: JWT-based; tokens in `Authorization: Bearer <token>` header
- **Frontend API Client**: Located at `/src/lib/api.ts`
- **Backend API Routes**: `/api/v1/tasks`, `/health` (as observed from current server logs)
- **Environment Variables**: BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEON_DATABASE_URL
- **Data Model**: Task entity with id, user_id, title, description, completed, created_at, updated_at

### Unknown Parameters (NEEDS CLARIFICATION)
- None (all parameters resolved in specification)

## Constitution Check

### Compliance Verification
- [x] User data isolation enforced via JWT user_id
- [x] No backend logic depends on frontend state
- [x] JWT enforcement applied from initial implementation
- [x] No trusted user input assumptions
- [x] No phase bypasses JWT enforcement

### Potential Violations
- None identified - all requirements align with constitution

## Research Phase (Phase 0)

### Task 0.1: Current API Mapping Analysis
- **Decision**: Analyze current API calls from frontend to backend
- **Rationale**: Need to understand the current mismatch between frontend requests and backend endpoints
- **Alternatives considered**: Manual inspection vs automated analysis

### Task 0.2: Better Auth Integration Patterns
- **Decision**: Research proper JWT handling between Better Auth and custom backend
- **Rationale**: Understanding how to securely pass JWT tokens from auth provider to backend
- **Alternatives considered**: Different authentication flow approaches

### Task 0.3: Next.js API Client Best Practices
- **Decision**: Identify best practices for API client implementation in Next.js
- **Rationale**: Proper integration requires following Next.js patterns and conventions
- **Alternatives considered**: Different HTTP client libraries and patterns

## Implementation Phases

### Phase 1: API Client Update

**Purpose**: Update the frontend API client to use correct backend endpoints and handle JWT tokens

**Deliverables**:
- `/src/lib/api.ts`: Updated API client with correct endpoints and JWT handling
- `/src/lib/types.ts`: Updated types to match backend data model
- `/src/contexts/UserContext.tsx`: Updated context to handle JWT tokens properly

**Logic Implemented**:
- Update base URL to include `/api/v1` prefix
- Automatically attach JWT token from user session to protected requests
- Handle 401 errors by redirecting to login
- Implement proper error handling for different response types

**Responsibilities**:
- Update API endpoints to match backend routes
- Handle JWT token attachment to requests
- Manage error responses appropriately
- Maintain backward compatibility with existing code

**Inputs**: Current API client code, backend endpoint documentation
**Outputs**: Updated API client with correct backend integration
**Completion Criteria**:
- API calls go to correct backend endpoints (`/api/v1/tasks`)
- JWT tokens are automatically attached to requests
- 401 errors are handled properly
- Error handling works for all response types

**Success Gates**:
- [ ] API client makes requests to correct endpoints
- [ ] JWT tokens attached automatically to requests
- [ ] 401 errors handled with login redirect
- [ ] Error handling works for all scenarios

### Phase 2: Task CRUD Operations Integration

**Purpose**: Integrate frontend task operations with backend API endpoints

**Deliverables**:
- Updated task service functions in frontend
- Proper task data model mapping between frontend and backend
- Error handling for task operations

**Logic Implemented**:
- Create task endpoint: POST `/api/v1/tasks`
- Read tasks endpoint: GET `/api/v1/tasks`
- Update task endpoint: PUT `/api/v1/tasks/{id}`
- Delete task endpoint: DELETE `/api/v1/tasks/{id}`
- Toggle completion: PATCH `/api/v1/tasks/{id}/complete`

**Responsibilities**:
- Map frontend task operations to backend endpoints
- Ensure proper data transformation between frontend and backend
- Handle task-specific error responses
- Maintain user data isolation

**Inputs**: Task operations from frontend components
**Outputs**: Successful task operations with backend integration
**Completion Criteria**:
- All task CRUD operations work with backend
- Data models match between frontend and backend
- User isolation maintained
- Proper error handling implemented

**Success Gates**:
- [ ] Create task works with backend
- [ ] Read tasks works with backend
- [ ] Update task works with backend
- [ ] Delete task works with backend
- [ ] Toggle completion works with backend

### Phase 3: Authentication Flow Integration

**Purpose**: Integrate Better Auth with backend API for proper JWT handling

**Deliverables**:
- Updated authentication context
- Proper JWT token extraction from Better Auth
- Session management between auth provider and backend

**Logic Implemented**:
- Extract JWT token from Better Auth session
- Pass token to backend API calls
- Handle token expiration and refresh
- Logout functionality that clears all sessions

**Responsibilities**:
- Connect Better Auth session with backend API
- Handle JWT token lifecycle
- Manage authentication state consistently
- Ensure secure token handling

**Inputs**: Better Auth session data
**Outputs**: Proper JWT token handling for backend API
**Completion Criteria**:
- JWT tokens extracted from Better Auth
- Tokens passed to backend API calls
- Token expiration handled properly
- Logout clears all sessions

**Success Gates**:
- [ ] JWT tokens extracted from Better Auth
- [ ] Tokens passed to API requests
- [ ] Token expiration handled
- [ ] Logout functionality works

### Phase 4: Error Handling & Validation

**Purpose**: Implement comprehensive error handling between frontend and backend

**Deliverables**:
- Global error handling implementation
- Specific error responses for different scenarios
- User-friendly error messages

**Logic Implemented**:
- Network error handling
- Server error (5xx) handling
- Validation error (4xx) handling
- Authentication error (401) handling

**Responsibilities**:
- Handle all types of API errors appropriately
- Provide clear feedback to users
- Maintain consistent error handling patterns
- Ensure graceful degradation

**Inputs**: Error responses from backend API
**Outputs**: Properly handled error states in frontend
**Completion Criteria**:
- All error types handled appropriately
- User-friendly error messages displayed
- Consistent error handling patterns
- Graceful degradation implemented

**Success Gates**:
- [ ] Network errors handled appropriately
- [ ] Server errors handled with user feedback
- [ ] Validation errors handled with field feedback
- [ ] Authentication errors trigger login redirect

### Phase 5: Data Model Consistency

**Purpose**: Ensure frontend and backend share consistent data models

**Deliverables**:
- Updated type definitions to match backend
- Proper data transformation between layers
- Consistent field naming and types

**Logic Implemented**:
- Task model consistency between frontend and backend
- Proper serialization/deserialization
- Field validation alignment
- Timestamp handling consistency

**Responsibilities**:
- Maintain data model consistency
- Handle data transformations properly
- Ensure field alignment
- Validate data types consistently

**Inputs**: Backend data model definitions
**Outputs**: Consistent data models between frontend and backend
**Completion Criteria**:
- Data models match between layers
- Proper transformations implemented
- Field alignment maintained
- Type validation consistent

**Success Gates**:
- [ ] Data models consistent between layers
- [ ] Transformations work properly
- [ ] Field alignment maintained
- [ ] Type validation consistent

### Phase 6: End-to-End Flow Testing

**Purpose**: Test complete user flows from authentication to task management

**Deliverables**:
- Complete flow testing documentation
- Identified and fixed integration issues
- Verified end-to-end functionality

**Logic Implemented**:
- Complete user journey testing
- Integration point verification
- Error scenario testing
- Performance validation

**Responsibilities**:
- Test complete user flows
- Verify all integration points
- Identify and fix issues
- Validate performance

**Inputs**: Complete user scenarios and test data
**Outputs**: Verified end-to-end functionality
**Completion Criteria**:
- Complete user flows tested successfully
- All integration points verified
- Issues identified and fixed
- Performance validated

**Success Gates**:
- [ ] Complete user flows work end-to-end
- [ ] All integration points verified
- [ ] Issues resolved
- [ ] Performance validated

### Phase 7: UI/UX Consistency

**Purpose**: Ensure frontend UI remains unchanged during integration

**Deliverables**:
- Verified UI components remain unchanged
- Loading/empty/error states work correctly
- Consistent user experience maintained

**Logic Implemented**:
- Maintain existing UI design
- Preserve component functionality
- Keep loading/error states working
- Ensure consistent UX

**Responsibilities**:
- Maintain existing UI design
- Preserve component functionality
- Keep states working correctly
- Ensure consistent UX

**Inputs**: Existing UI components and designs
**Outputs**: Integrated functionality with unchanged UI
**Completion Criteria**:
- UI design remains unchanged
- Component functionality preserved
- States work correctly
- UX remains consistent

**Success Gates**:
- [ ] UI design unchanged
- [ ] Component functionality preserved
- [ ] Loading/error states work
- [ ] UX remains consistent

## Success Criteria Verification

Upon completion of all phases:
- [ ] Users can perform complete task management flow with 99% success rate
- [ ] Authentication flow completes successfully with 99% success rate
- [ ] API requests include proper JWT tokens with 100% reliability
- [ ] 401 Unauthorized errors trigger proper login redirects with 100% reliability
- [ ] Error handling provides clear user feedback for 100% of error scenarios
- [ ] Data consistency is maintained between frontend and backend with 100% accuracy
- [ ] Frontend UI remains unchanged during integration
- [ ] End-to-end flow works without errors
- [ ] All existing frontend components continue to function correctly after integration
- [ ] Loading, empty, and error states work correctly during API communication