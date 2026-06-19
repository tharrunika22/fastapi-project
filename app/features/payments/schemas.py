from pydantic import BaseModel


class RazorpayOrderCreate(BaseModel):
    amount: int


class RazorpayOrderResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
class PaymentVerification(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str 
    user_id: int 
    amount:int