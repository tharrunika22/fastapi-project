from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.users.models import User
from app.features.users.schemas import UserCreate, UserUpdate 
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/")
def create_user(data: UserCreate, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(User.email == data.email).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    existing_phone = db.query(User).filter(User.phone == data.phone).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone already exists"
        )

    hashed_password = hash_password(data.password)

    user = User(
        username=data.username,
        email=data.email,
        phone=data.phone,
        password=hashed_password,
        role=data.role
 )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all() 
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user 
@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            value = hash_password(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user 
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}