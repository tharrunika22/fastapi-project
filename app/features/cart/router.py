from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.features.cart.schemas import CartCreate

from app.features.cart.service import (
    add_to_cart,
    get_user_cart,
    remove_from_cart
)

from app.core.security import get_current_user   # ✅ FIXED IMPORT

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/")
def create_cart(
    data: CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return add_to_cart(
        db,
        current_user.id,
        data
    )


@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_cart(
        db,
        current_user.id
    )


@router.delete("/{cart_id}")
def delete_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = remove_from_cart(db, cart_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return {
        "message": "Item removed from cart"
    } 
