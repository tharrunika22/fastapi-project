from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from . import service
from .schemas import PaymentVerification 
from app.features.payments.models import Payment 
from app.db.session import get_db


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


class CreateOrderRequest(BaseModel):
    amount: int


@router.post("/create-razorpay-order")
def create_razorpay_order(data: CreateOrderRequest):
    """Create a Razorpay order from the provided amount (in whole currency units).

    Example request body: {"amount": 200}
    """

    order = service.create_razorpay_order(data.amount)

    return order 
@router.post("/verify-payment")
def verify_payment(data: PaymentVerification, db: Session = Depends(get_db)):

    is_verified = service.verify_payment(
        data.razorpay_order_id,
        data.razorpay_payment_id,
        data.razorpay_signature
    )

    if not is_verified:

        payment = Payment( 
            user_id=data.user_id,
            razorpay_order_id=data.razorpay_order_id,
            razorpay_payment_id=data.razorpay_payment_id,
            amount=data.amount,
            status="FAILED"
        )

        db.add(payment)
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed"
        )

    payment = Payment( 
        user_id=data.user_id,
        razorpay_order_id=data.razorpay_order_id,
        razorpay_payment_id=data.razorpay_payment_id,
        amount=data.amount,
        status="SUCCESS"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "verified": True,
        "payment_id": payment.id,
        "message": "Payment verified successfully"
    }