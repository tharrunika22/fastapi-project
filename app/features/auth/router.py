from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from jose import JWTError

from app.db.session import get_db
from app.features.users.models import User 
from app.core.security import get_current_user 
from app.core.security import create_refresh_token 
from app.core.security import decode_access_token, create_access_token

from app.features.auth.schemas import (
    SignupRequest,
    LoginRequest, 
    VerifyEmailRequest, 
    ChangePasswordRequest, 
    ResetPasswordRequest,
    RefreshTokenRequest
)

from app.features.auth.service import (
    create_user,
    authenticate_user,
    change_password,
    reset_password,
   
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
    refresh_token = create_refresh_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    } 
@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest
):

    try:

        payload = decode_access_token(
            data.refresh_token
        )

        if payload.get("type") != "refresh":

            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")

        new_access_token = create_access_token(
            {"sub": user_id}
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
@router.post("/verify-email")
def verify_email(
    data: VerifyEmailRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    return {
        "message": "Email verified"
    } 

@router.post("/reset-password")
def reset_password_route(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    return reset_password(
        data,
        db
    )

@router.put("/change-password")
def change_password_route(
    data: ChangePasswordRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return change_password(
        current_user,
        data,
        db
    )
@router.post("/logout")
def logout():

    return {
        "message": "Logout successful"
    }