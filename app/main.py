from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.features.products.models import Product
from app.features.products.router import router as product_router

from app.features.orders.models import Order
from app.features.orders.router import router as order_router 

from app.features.users.models import User
from app.features.users.router import router as user_router 
from app.features.auth.router import router as auth_router 
from app.features.cart.router import (
    router as cart_router
)


Base.metadata.create_all(bind=engine)


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(order_router) 
app.include_router(user_router) 
app.include_router(auth_router)
app.include_router(cart_router)
@app.get("/")
def home():
    return {"message": "Ecommerce API Running"}