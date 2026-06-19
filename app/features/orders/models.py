from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    payment_id = Column(
        Integer,
        ForeignKey("payments.id")
    )

    quantity = Column(Integer)

    ordered_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    payment_status = Column(
        String,
        default="Pending"
    )

    razorpay_order_id = Column(
        String,
        nullable=True
    )

    razorpay_payment_id = Column(
        String,
        nullable=True
    )

    razorpay_signature = Column(
        String,
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    product = relationship(
        "Product",
        back_populates="orders"
    ) 
    