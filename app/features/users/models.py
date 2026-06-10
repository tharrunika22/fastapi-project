from sqlalchemy import Column, Integer, String
from app.db.base import Base 
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    username = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    phone = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False) 
    orders = relationship("Order", back_populates="user") 
    role = Column(String, nullable=False)