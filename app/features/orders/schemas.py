from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int 
    address: str  
    razorpay_order_id: str | None = None 
    razorpay_payment_id: str | None = None
    razorpay_signature: str | None = None
class OrderUpdate(BaseModel):
    user_id: int
    product_id: int
    quantity: int