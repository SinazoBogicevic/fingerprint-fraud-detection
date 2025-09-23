"""
auth api endpoints for the auth service
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.auth import login_user, register_user
from database import get_db

router = APIRouter()


class UserRegister(BaseModel):
    """
    User register model
    """

    email: str
    hashed_password: str


class UserLogin(BaseModel):
    """
    User login model
    """

    email: str
    hashed_password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_endpoint(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    return register_user(user.email, user.hashed_password, db)


@router.post("/login")
def login_endpoint(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user
    """
    return login_user(user.email, user.hashed_password, db)
