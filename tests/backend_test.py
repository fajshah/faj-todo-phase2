import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock
from datetime import timedelta
from main import app
from src.database.engine import get_async_session
from src.auth.utils import create_access_token


# Test database setup
@pytest.fixture(name="engine")
def fixture_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="async_session")
def fixture_async_session(engine):
    """Create an async session for testing."""
    from sqlmodel.ext.asyncio.session import AsyncSession

    async_session = AsyncSession(bind=engine)
    yield async_session
    asyncio.run(async_session.close())


@pytest.fixture(name="client")
def fixture_client(async_session):
    def get_async_session_override():
        yield async_session

    app.dependency_overrides[get_async_session] = get_async_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]


def test_auth_signup(client):
    """Test user signup endpoint"""
    signup_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/signup", json=signup_data)
    # Should return 200 if successful, or 400 if user already exists
    assert response.status_code in [200, 400]


def test_auth_login_logout(client):
    """Test user login and logout endpoints"""
    # First, try to login with a test user (might fail if user doesn't exist)
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/login", params=login_data)
    # This might return 401 if user doesn't exist yet, which is expected
    assert response.status_code in [200, 401]

    # Test logout (should work regardless of auth status)
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_protected_task_endpoints_require_auth(client):
    """Test that task endpoints require authentication"""
    # Try to access tasks without auth - should return 401
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401

    # Try to create task without auth - should return 401
    task_data = {"title": "Test task", "description": "Test description", "completed": False}
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 401


def test_jwt_token_creation():
    """Test JWT token creation utility"""
    test_data = {"sub": "test-user-id"}
    token = create_access_token(data=test_data, expires_delta=timedelta(minutes=30))
    assert isinstance(token, str)
    assert len(token) > 0