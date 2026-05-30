from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.features.products.models import Product
from app.features.products.router import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router)

@app.get("/")
def home():
    return {"message": "Ecommerce API Running"}