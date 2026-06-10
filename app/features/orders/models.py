from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base 
from sqlalchemy.orm import relationship 
from sqlalchemy import DateTime
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer) 
    ordered_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    user = relationship("User", back_populates="orders")
    product = relationship("Product")