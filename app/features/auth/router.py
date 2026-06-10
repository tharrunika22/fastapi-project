from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.features.auth.schemas import (
    SignupRequest,
    LoginRequest
)

from app.features.auth.service import (
    create_user,
    authenticate_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):

    create_user(data, db)

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    token, user = authenticate_user(
        data,
        db
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/logout")
def logout():

    return {
        "message": "Logout successful"
    }