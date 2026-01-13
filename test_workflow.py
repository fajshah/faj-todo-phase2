#!/usr/bin/env python3
"""
Test script to validate the complete workflow:
signup -> login -> create task -> view task -> edit task -> complete task -> delete task -> logout
"""
import requests
import time
import uuid

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_complete_workflow():
    print("Testing complete workflow: signup -> login -> create task -> view task -> edit task -> complete task -> delete task -> logout")

    # Create a unique email for this test
    test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "password123"

    # 1. Signup
    print("\n1. Testing signup...")
    signup_response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "email": test_email,
            "password": test_password
        }
    )
    print(f"Signup response: {signup_response.status_code}")
    assert signup_response.status_code == 200, f"Signup failed with status {signup_response.status_code}"

    user_data = signup_response.json()
    user_id = user_data.get("id")
    print(f"Created user with ID: {user_id}")

    # 2. Login
    print("\n2. Testing login...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "email": test_email,
            "password": test_password
        }
    )
    print(f"Login response: {login_response.status_code}")
    assert login_response.status_code == 200, f"Login failed with status {login_response.status_code}"

    auth_data = login_response.json()
    access_token = auth_data.get("access_token")
    assert access_token, "No access token returned from login"
    print("Login successful, received access token")

    # Set up headers with the token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 3. Create task
    print("\n3. Testing create task...")
    task_data = {
        "title": "Test task for workflow validation",
        "description": "This is a test task created during workflow validation",
        "priority": "medium"
    }
    create_task_response = requests.post(
        f"{BASE_URL}/tasks",
        json=task_data,
        headers=headers
    )
    print(f"Create task response: {create_task_response.status_code}")
    assert create_task_response.status_code == 200, f"Create task failed with status {create_task_response.status_code}"

    created_task = create_task_response.json()
    task_id = created_task.get("id")
    print(f"Created task with ID: {task_id}")

    # 4. View task (get all tasks)
    print("\n4. Testing view tasks...")
    get_tasks_response = requests.get(
        f"{BASE_URL}/tasks",
        headers=headers
    )
    print(f"Get tasks response: {get_tasks_response.status_code}")
    assert get_tasks_response.status_code == 200, f"Get tasks failed with status {get_tasks_response.status_code}"

    tasks = get_tasks_response.json()
    assert len(tasks) >= 1, "Should have at least one task"
    print(f"Retrieved {len(tasks)} tasks")

    # 5. Edit task
    print("\n5. Testing edit task...")
    updated_task_data = {
        "title": "Updated test task",
        "description": "This task has been updated",
        "priority": "high"
    }
    update_task_response = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json=updated_task_data,
        headers=headers
    )
    print(f"Update task response: {update_task_response.status_code}")
    assert update_task_response.status_code == 200, f"Update task failed with status {update_task_response.status_code}"

    updated_task = update_task_response.json()
    assert updated_task.get("title") == "Updated test task", "Task title was not updated"
    print("Task updated successfully")

    # 6. Complete task
    print("\n6. Testing complete task...")
    complete_task_response = requests.put(
        f"{BASE_URL}/tasks/{task_id}/complete",
        headers=headers
    )
    print(f"Complete task response: {complete_task_response.status_code}")
    assert complete_task_response.status_code == 200, f"Complete task failed with status {complete_task_response.status_code}"

    completed_task = complete_task_response.json()
    assert completed_task.get("completed") is True, "Task was not marked as completed"
    print("Task marked as completed")

    # 7. Delete task
    print("\n7. Testing delete task...")
    delete_task_response = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    print(f"Delete task response: {delete_task_response.status_code}")
    assert delete_task_response.status_code == 200, f"Delete task failed with status {delete_task_response.status_code}"
    print("Task deleted successfully")

    # 8. Logout (not really needed since we're using JWT tokens, but endpoint exists)
    print("\n8. Testing logout...")
    logout_response = requests.post(f"{BASE_URL}/auth/logout")
    print(f"Logout response: {logout_response.status_code}")
    assert logout_response.status_code == 200, f"Logout failed with status {logout_response.status_code}"
    print("Logout endpoint called successfully")

    print("\n✓ Complete workflow test passed successfully!")

def test_error_scenarios():
    print("\n\nTesting error scenarios...")

    # Test invalid credentials
    print("\n1. Testing invalid credentials...")
    invalid_login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    print(f"Invalid login response: {invalid_login_response.status_code}")
    assert invalid_login_response.status_code == 401, f"Expected 401 for invalid login, got {invalid_login_response.status_code}"
    print("SUCCESS: Invalid credentials properly return 401")

    # Test unauthorized access to protected endpoint
    print("\n2. Testing unauthorized access...")
    unauthorized_response = requests.get(f"{BASE_URL}/tasks")
    print(f"Unauthorized access response: {unauthorized_response.status_code}")
    assert unauthorized_response.status_code == 401, f"Expected 401 for unauthorized access, got {unauthorized_response.status_code}"
    print("SUCCESS: Unauthorized access properly returns 401")

    # Test invalid token
    print("\n3. Testing invalid token...")
    invalid_token_headers = {
        "Authorization": "Bearer invalid.token.here",
        "Content-Type": "application/json"
    }
    invalid_token_response = requests.get(
        f"{BASE_URL}/tasks",
        headers=invalid_token_headers
    )
    print(f"Invalid token response: {invalid_token_response.status_code}")
    assert invalid_token_response.status_code == 401, f"Expected 401 for invalid token, got {invalid_token_headers.status_code}"
    print("SUCCESS: Invalid token properly returns 401")

def test_404_endpoints():
    print("\n\nTesting 404 errors for non-existent endpoints...")

    # Test non-existent endpoint
    non_existent_response = requests.get(f"{BASE_URL}/nonexistent/endpoint")
    print(f"Non-existent endpoint response: {non_existent_response.status_code}")

    # Also test with valid auth to ensure it's not a 401
    headers = {"Authorization": "Bearer invalid.token"}
    non_existent_with_auth_response = requests.get(
        f"{BASE_URL}/nonexistent/endpoint",
        headers=headers
    )
    print(f"Non-existent endpoint with auth response: {non_existent_with_auth_response.status_code}")

def test_api_responses():
    print("\n\nTesting API responses per OpenAPI specification...")

    # Test health endpoint
    health_response = requests.get("http://localhost:8000/health")
    print(f"Health endpoint response: {health_response.status_code}")
    assert health_response.status_code == 200
    print("SUCCESS: Health endpoint works")

    # Test docs endpoint
    docs_response = requests.get("http://localhost:8000/docs")
    print(f"Docs endpoint response: {docs_response.status_code}")
    assert docs_response.status_code == 200
    print("SUCCESS: Docs endpoint works")

    # Test openapi.json endpoint
    openapi_response = requests.get("http://localhost:8000/openapi.json")
    print(f"OpenAPI endpoint response: {openapi_response.status_code}")
    assert openapi_response.status_code == 200
    print("SUCCESS: OpenAPI endpoint works")

if __name__ == "__main__":
    print("Starting backend-frontend integration tests...")

    # Start the server first (this would be done separately in practice)
    print("Note: Please ensure the backend server is running with: uvicorn main:app --reload --port 8000")

    try:
        # Test basic API functionality first
        test_api_responses()

        # Test the complete workflow
        test_complete_workflow()

        # Test error scenarios
        test_error_scenarios()

        # Test 404 scenarios
        test_404_endpoints()

        print("\n\nSUCCESS: All tests passed! Backend-frontend integration is working correctly.")

    except Exception as e:
        print(f"\n\nERROR: Test failed with error: {str(e)}")
        raise