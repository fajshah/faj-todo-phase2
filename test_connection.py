import asyncio
import httpx

async def test_backend():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test the root endpoint
            response = await client.get("http://127.0.0.1:8000/")
            print(f"Root endpoint status: {response.status_code}")
            print(f"Root endpoint response: {response.text[:200]}...")

            # Test the docs endpoint
            response = await client.get("http://127.0.0.1:8000/docs")
            print(f"Docs endpoint status: {response.status_code}")

            # Test the health endpoint
            response = await client.get("http://127.0.0.1:8000/health")
            print(f"Health endpoint status: {response.status_code}")
            if response.status_code == 200:
                print(f"Health response: {response.json()}")

    except Exception as e:
        print(f"Error connecting to backend: {e}")

if __name__ == "__main__":
    asyncio.run(test_backend())