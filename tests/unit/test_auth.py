from fastapi.testclient import TestClient


def test_register_user_success(client: TestClient):
    """
    Test the register user success
    """
    payload = {"email": "test@test.com", "hashed_password": "Test1234567890!"}

    response = client.post("/auth/register", json=payload)

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "user_id" in data
    assert data["message"] == "User registered successfully"
