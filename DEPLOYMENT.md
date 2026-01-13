# Deployment Instructions

## Local Development

### Prerequisites
- Python 3.13+
- pip package manager

### Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```
5. Update the `.env` file with your specific configuration

### Running Locally
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

### Environment Configuration
- Set `NEON_DATABASE_URL` to your production database URL
- Set `BETTER_AUTH_SECRET` to a strong, randomly generated secret
- Adjust logging level as needed (recommended: `INFO` or `WARNING`)

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t todo-backend .
docker run -d -p 8000:8000 --env-file .env todo-backend
```

### Cloud Deployment (AWS/GCP/Azure)

#### Heroku Example
1. Create `Procfile`:
   ```
   web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}
   ```

2. Set environment variables in Heroku dashboard:
   - `NEON_DATABASE_URL`
   - `BETTER_AUTH_SECRET`

#### AWS Elastic Beanstalk
1. Create application bundle with:
   - `application.py` (or `main.py`)
   - `requirements.txt`
   - `Procfile` (if using EB CLI)

### Postgres Configuration
To use PostgreSQL instead of SQLite:
1. Set `NEON_DATABASE_URL` to your PostgreSQL connection string:
   ```
   postgresql://username:password@host:port/database_name
   ```
2. The application will automatically use asyncpg for PostgreSQL connections

## Health Checks
- Basic health: `GET /health`
- Database connectivity: `GET /health/database`

## Monitoring
- Monitor application logs for errors
- Set up alerts for health check failures
- Track response times and error rates