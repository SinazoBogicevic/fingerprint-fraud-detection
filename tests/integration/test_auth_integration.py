import uuid

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


def test_persists_user(client: TestClient, db_session: Session):
    """
    Test that the user is persisted in the database
    """

    payload = {"email": "test@test.com", "hashed_password": "Test1234567890!"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == payload["email"]
    assert "user_id" in body

    return_id = body["user_id"]

    stmt = select(User).where(User.id == uuid.UUID(return_id))

    user_row = db_session.execute(stmt).scalars().first()

    assert user_row is not None, "User not found in the database"

    assert str(user_row.email) == payload["email"]

    assert str(user_row.hashed_password) == payload["hashed_password"]
