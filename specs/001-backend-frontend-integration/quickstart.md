# Quickstart Guide: Backend-Frontend Integration

## Development Environment Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or Neon Serverless account)

### Backend Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update .env with your actual values:
   # BETTER_AUTH_SECRET=your_secret_key
   # BETTER_AUTH_URL=http://localhost:3000
   # NEON_DATABASE_URL=your_neon_database_url
   ```

4. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Create new user
- `POST /api/v1/auth/login` - Authenticate user
- `POST /api/v1/auth/logout` - Logout user

### Tasks
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PUT /api/v1/tasks/{id}/complete` - Toggle task completion

## Common Issues & Solutions

### Backend Not Starting
- Check that all dependencies in requirements.txt are installed
- Verify Python path and virtual environment activation
- Ensure main.py is in the correct location

### 404 Errors
- Verify API route prefixes match frontend expectations
- Check that routers are properly registered in main.py
- Confirm endpoint paths match the contract specification

### CORS Issues
- Ensure CORS middleware is properly configured in main.py
- Check that frontend origin is allowed in backend settings

### Database Connection
- Verify NEON_DATABASE_URL is correctly set in environment
- Ensure async database engine is properly configured
- Check that SQLModel models are correctly defined