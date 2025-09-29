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


def test_register_user_failure(client: TestClient):
    """
    Test the register user failure
    """
    payload = {"email": "test@test.com", "hashed_password": "Test1234567890!"}

    response = client.post("/auth/register", json=payload)

    replica = {"email": "test@test.com", "hashed_password": "Test1234567890!"}

    response = client.post("/auth/register", json=replica)
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "User already exists"


def test_register_user_failure_invalid_email(client: TestClient):
    """
    Test the register user failure invalid email
    """
    payload = {"email": "test@test.c", "hashed_password": "Test1234567890!"}

    response = client.post("/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Invalid email format"


def test_register_user_failure_invalid_password(client: TestClient):
    """
    Test the register user failure invalid password
    """
    payload = {"email": "test@test.com", "hashed_password": "1234567890!"}

    response = client.post("/auth/register", json=payload)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Invalid password format"
