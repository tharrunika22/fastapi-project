from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.features.users.models import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def create_user(data, db: Session):

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

    user = User(
        username=data.username,
        email=data.email,
        phone=data.phone,
        password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(data, db: Session):

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

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username
        }
    )

    return token, user