# Phase 2 Backend - Todo App

This is the backend server for the Phase 2 Todo Application, built with Node.js, Express, and MongoDB.

## Features

- JWT-based authentication (register/login)
- Todo CRUD operations
- Password hashing with bcrypt
- Input validation
- Error handling
- Rate limiting
- CORS support
- Environment-based configuration

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user and get JWT token

### Todos
- `GET /api/todos` - Get all user's todos (requires auth)
- `GET /api/todos/:id` - Get a specific todo (requires auth)
- `POST /api/todos` - Create a new todo (requires auth)
- `PUT /api/todos/:id` - Update a todo (requires auth)
- `DELETE /api/todos/:id` - Delete a todo (requires auth)

## Setup Instructions

1. Clone the repository
2. Navigate to the backend directory: `cd phase-2/backend`
3. Install dependencies: `npm install`
4. Create a `.env` file based on `.env.example`
5. Start the server: `npm run dev` (for development) or `npm start` (for production)

## Environment Variables

Create a `.env` file in the backend root directory with the following variables:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/todoapp

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

## Deployment

The backend is ready for deployment to platforms like Heroku, AWS, or Google Cloud. Make sure to set the environment variables in your deployment platform.

## Dependencies

- express: Web framework
- mongoose: MongoDB object modeling
- bcryptjs: Password hashing
- jsonwebtoken: JWT implementation
- cors: Cross-origin resource sharing
- helmet: Security headers
- morgan: HTTP request logger
- express-rate-limit: Rate limiting
- dotenv: Environment variables management