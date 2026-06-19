
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    razorpay_order_id = Column(String, nullable=False)

    razorpay_payment_id = Column(String, nullable=True)

    amount = Column(Float, nullable=False)

    status = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )