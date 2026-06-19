from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.features.address.schemas import (
    AddressCreate,
    AddressResponse,
)

from app.features.address.service import (
    create_address,
    get_user_addresses,
    update_address,
    delete_address,
)

from app.core.security import get_current_user

router = APIRouter(
    prefix="/address",
    tags=["Address"]
)


@router.post("/", response_model=AddressResponse)
def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_address(
        db=db,
        user_id=current_user.id,
        data=data
    )


@router.get("/", response_model=list[AddressResponse])
def get_addresses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_addresses(
        db=db,
        user_id=current_user.id
    )


@router.put("/{address_id}", response_model=AddressResponse)
def edit_address(
    address_id: int,
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    address = update_address(
        db=db,
        address_id=address_id,
        user_id=current_user.id,
        data=data
    )

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    return address


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = delete_address(
        db=db,
        address_id=address_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    return {
        "message": "Address deleted successfully"
    }