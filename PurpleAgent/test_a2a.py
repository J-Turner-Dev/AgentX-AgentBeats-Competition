"""
Test the A2A server locally
"""

import requests
import json
import time


def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)

    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    assert response.status_code == 200
    print("✓ Health check passed")


def test_assess():
    """Test assessment endpoint"""
    print("\n" + "=" * 60)
    print("Testing Assessment Endpoint")
    print("=" * 60)

    # Test request
    request_data = {
        "task": "Analyze sentiment for: iPhone 16",
        "config": {"max_time": 60, "return_details": True},
    }

    print(f"\nRequest: {json.dumps(request_data, indent=2)}")

    start = time.time()
    response = requests.post(
        "http://localhost:8000/assess",
        json=request_data,
        headers={"Content-Type": "application/json"},
    )
    elapsed = time.time() - start

    print(f"\nStatus: {response.status_code}")
    print(f"Time: {elapsed:.1f}s")
    print(f"\nResponse: {json.dumps(response.json(), indent=2)}")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "result" in data
    assert data["result"]["topic"] == "iPhone 16"

    print("✓ Assessment test passed")


def test_multiple_topics():
    """Test multiple assessments"""
    print("\n" + "=" * 60)
    print("Testing Multiple Topics")
    print("=" * 60)

    topics = ["ChatGPT", "remote work", "electric vehicles"]

    for topic in topics:
        print(f"\n  Testing: {topic}")

        response = requests.post(
            "http://localhost:8000/assess",
            json={"task": f"Analyze sentiment for: {topic}"},
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                result = data["result"]
                print(f"    ✓ {result['sentiment']} ({result['confidence']:.0%})")
            else:
                print(f"    ✗ Failed: {data.get('error')}")
        else:
            print(f"    ✗ HTTP {response.status_code}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("A2A SERVER TESTING")
    print("=" * 60)
    print("\nMake sure server is running:")
    print("  python a2a_server.py")
    print("\nPress Enter when ready...")
    input()

    try:
        test_health()
        test_assess()
        test_multiple_topics()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
