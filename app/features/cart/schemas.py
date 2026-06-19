from pydantic import BaseModel


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class ProductOut(BaseModel):
    name: str
    price: float
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True