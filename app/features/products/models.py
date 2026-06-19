from sqlalchemy import Column, ForeignKey, Integer, String, Float 
from sqlalchemy.orm import relationship 
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer) 
    vendor_id = Column(Integer,ForeignKey("users.id") )

    vendor = relationship(
        "User",
         back_populates="products") 
    images = relationship(
    "ProductImage",
    back_populates="product",
    cascade="all, delete"
)
    orders = relationship(
        "Order",
        back_populates="product"
    )
    carts = relationship(
        "Cart",
        back_populates="product"
    )
