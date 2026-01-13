# Research Document: Phase II Todo Backend API

**Feature**: 1-backend-todo-api
**Created**: 2026-01-01-08
**Status**: Complete

## Research Task 0.1: JWT Token Structure Research

**Decision**: Better Auth JWT token structure follows standard JWT format with user_id in the subject claim
**Rationale**: Better Auth typically places user identifier in the "sub" (subject) claim of JWT tokens, which is the standard practice for user identification
**Alternatives considered**:
- Custom claims like "userId" or "user_id" - less standard
- Nested claims in "user" object - adds complexity
**Finding**: JWT tokens will have user_id in the "sub" claim following standard JWT practices

## Research Task 0.2: Neon PostgreSQL Connection Best Practices

**Decision**: Use connection pooling with reasonable limits and timeouts for Neon Serverless
**Rationale**: Neon's serverless architecture benefits from connection reuse but requires careful pool management to avoid connection exhaustion
**Alternatives considered**:
- Direct connections without pooling - inefficient
- Large pool sizes - may exceed Neon limits
**Finding**: Optimal settings include pool size of 10-20 connections with appropriate timeouts for serverless architecture

## Research Task 0.3: FastAPI Security Patterns

**Decision**: Implement JWT verification using FastAPI dependencies with python-jose
**Rationale**: FastAPI dependencies provide clean integration with JWT verification while maintaining proper error handling
**Alternatives considered**:
- Middleware approach - less flexible
- Decorator pattern - harder to maintain
**Finding**: FastAPI security dependencies offer the best balance of functionality and maintainability

## Research Task 0.4: SQLModel Relationship Patterns

**Decision**: Use user_id as string field with proper indexing for efficient filtering
**Rationale**: Storing user_id as string allows flexibility while proper indexing ensures efficient user-based queries
**Alternatives considered**:
- Foreign key relationships - unnecessary complexity for JWT-based user identification
- Additional user table - not required for this implementation
**Finding**: Direct user_id storage with indexing provides optimal performance for user isolation

## Resolution of NEEDS CLARIFICATION Items

### Previously Unknown: Specific JWT token structure from Better Auth
**Now Known**: JWT tokens contain user_id in the "sub" claim following standard JWT practices
**Impact**: Implementation will extract user_id from token["sub"]

### Previously Unknown: Exact database connection pooling settings
**Now Known**: Pool size of 10-20 connections with appropriate timeouts for Neon Serverless
**Impact**: Database engine will be configured with these optimal settings

### Previously Unknown: CORS configuration specifics beyond frontend origin
**Now Known**: Standard CORS configuration allowing localhost:3000 with Authorization header support
**Impact**: CORS middleware will be configured with these specific settings

### Previously Unknown: Database connection timeout settings
**Now Known**: Reasonable timeouts of 30 seconds for connect and command execution
**Impact**: Database engine will use these timeout values

### Previously Unknown: Specific error response format preferences
**Now Known**: JSON format with "detail" field following FastAPI conventions
**Impact**: Error handlers will return consistent JSON responses with "detail" field