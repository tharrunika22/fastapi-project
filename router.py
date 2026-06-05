from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.users.models import User
from app.core.security import (
    verify_password,
    create_access_token
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


from app.features.auth.schemas import (
    SignupRequest,
    LoginRequest,
)

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    existing_phone = db.query(User).filter(
        User.phone == data.phone
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone already exists"
        )

    from app.core.security import hash_password

    user = User(
        username=data.username,
        email=data.email,
        phone=data.phone,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():

    return {
        "message": "Logout successful"
    }