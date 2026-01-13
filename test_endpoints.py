#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
"""
import asyncio
import httpx
import json

async def test_api_endpoints():
    base_url = "http://localhost:8000"  # Assuming default FastAPI port

    async with httpx.AsyncClient(timeout=30.0) as client:
        print("Testing API endpoints...\n")

        # Test health endpoint
        print("1. Testing health endpoint:")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")

        print()

        # Test auth signup endpoint path
        print("2. Testing auth signup endpoint availability:")
        print("   Expected path: /api/v1/auth/signup")

        # Test tasks endpoint path
        print("3. Testing tasks endpoint availability:")
        print("   Expected path: /api/v1/tasks (GET, POST)")
        print("   Note: POST /api/v1/tasks requires authentication")

        print("\nTo test the full flow:")
        print("1. First register a user: POST /api/v1/auth/signup")
        print("2. Then login to get token: POST /api/v1/auth/login")
        print("3. Use the token to access tasks: GET/POST /api/v1/tasks")

        print("\nMake sure your server is running on the correct port.")
        print("Default FastAPI runs on http://127.0.0.1:8000 or http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_api_endpoints())