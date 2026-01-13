# Deployment Notes: Todo App - Phase II

## Project Structure

The project has been restructured into two separate deployable units:

```
├── backend/                  # Python FastAPI backend
│   ├── main.py               # Main application file
│   ├── api/                  # API routes (v1)
│   ├── auth/                 # Authentication logic
│   ├── database/             # Database configuration
│   ├── models/               # Data models
│   ├── services/             # Business logic services
│   ├── controllers/          # API controllers
│   ├── schemas/              # Pydantic schemas
│   ├── validators/           # Input validators
│   ├── errors/               # Custom exceptions
│   ├── middleware/           # Middleware components
│   ├── checks/               # Code quality/performance checks
│   ├── deployment/           # Deployment configurations
│   ├── integration/          # Integration tests/configs
│   ├── v1/                   # Version 1 configs
│   ├── __init__.py           # Package marker
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   ├── .env.example          # Environment variables template
│   └── README.md             # Backend documentation
├── frontend/                 # Next.js frontend
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   ├── contexts/             # React contexts
│   ├── hooks/                # React hooks
│   ├── layouts/              # Layout components
│   ├── modules/              # Shared modules
│   ├── pages/                # Next.js pages
│   ├── shared/               # Shared utilities
│   ├── styles/               # CSS styles
│   ├── utils/                # Utility functions
│   ├── src/                  # Additional source files
│   ├── .env.local            # Local environment variables
│   ├── next.config.js        # Next.js configuration
│   ├── next-env.d.ts         # TypeScript definitions
│   ├── postcss.config.js     # PostCSS configuration
│   ├── tailwind.config.ts    # Tailwind CSS configuration
│   ├── tsconfig.json         # TypeScript configuration
│   ├── package.json          # Node.js dependencies
│   ├── package-lock.json     # Locked dependencies
│   └── README.md             # Frontend documentation
└── DEPLOYMENT_NOTES.md       # This file
```

## Backend Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your configuration:
   - `NEON_DATABASE_URL`: Database connection URL (default: SQLite)
   - `BETTER_AUTH_SECRET`: Secret key for JWT authentication
   - `FRONTEND_URL`: Frontend origin URL for CORS
   - `CORS_ALLOW_ORIGINS`: Additional allowed origins (comma-separated)

### Running the Backend
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be accessible at `http://localhost:8000`

## Frontend Setup

### Prerequisites
- Node.js 18+
- npm or yarn package manager

### Installation
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies:
   ```bash
   npm install
   ```

### Configuration
The frontend is configured to communicate with the backend API at `http://localhost:8000/api/v1` by default via the `NEXT_PUBLIC_API_URL` environment variable in `.env.local`.

### Running the Frontend
```bash
npm run dev
```

The frontend will be accessible at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Tasks
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{id}` - Get a specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle task completion

### Health
- `GET /health` - Health check
- `GET /health/database` - Database health check

## Deployment

### Backend Deployment
1. Ensure all environment variables are set appropriately for your deployment environment
2. Use a WSGI/ASGI server like Gunicorn for production:
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment
1. Build the application:
   ```bash
   npm run build
   ```
2. Serve the built application with a web server like Nginx

## CORS Configuration
The backend is configured to allow requests from the frontend origin specified in the environment variables. The default configuration allows requests from `http://localhost:3000`.