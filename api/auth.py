import re
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt  # type: ignore
from sqlalchemy.orm import Session

from models.user import User


def register_user(email: str, hashed_password: str, db: Session):
    """
    Register a new user
    """
    if not email and not hashed_password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        hashed_password,
    ):
        raise HTTPException(status_code=400, detail="Invalid password format")

    if check_user_exists(email, db):
        raise HTTPException(status_code=409, detail="User already exists")

    try:
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {
            "message": "User registered successfully",
            "user_id": str(user.id),
            "email": user.email,
        }
    finally:
        db.close()


def login_user(email: str, hashed_password: str, db: Session):
    """
    Login a user
    """
    if not email and not hashed_password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        hashed_password,
    ):
        raise HTTPException(status_code=400, detail="Invalid password format")
    if not check_user_exists(email, db):
        raise HTTPException(status_code=401, detail="User doesn't exist")

    try:
        user = (
            db.query(User)
            .filter(User.email == email, User.hashed_password == hashed_password)
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        return {
            "token_type": "Bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    finally:
        db.close()


def check_user_exists(email: str, db: Session):
    """
    Check if a user exists in the database
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        return user is not None
    finally:
        db.close()


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_minutes: int = 15) -> str:
    """
    Create an access token
    """

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = {"exp": expire, "sub": user_id, "type": "access"}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore


def create_refresh_token(user_id: str, expires_days: int = 7) -> str:
    """
    Create a refresh token
    """

    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)

    payload = {"exp": expire, "sub": user_id, "type": "refresh"}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
