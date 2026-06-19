from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.features.orders.models import Order
from app.features.orders.schemas import  OrderCreate
from fastapi import APIRouter, Depends, HTTPException
from app.features.orders.schemas import OrderCreate, OrderUpdate 
from app.features.products.models import Product
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/")
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db)
    
):
    order = Order(
        user_id=data.user_id,
        product_id=data.product_id,
        quantity=data.quantity,
        payment_status="Paid",
        razorpay_order_id=data.razorpay_order_id,
        razorpay_payment_id=data.razorpay_payment_id,
        razorpay_signature=data.razorpay_signature
)


    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all() 
@router.get("/user/{user_id}")
def get_orders_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(
        Order.user_id == user_id
    ).all()
    result = []

    for order in orders:
        result.append({
           "id": order.id,
            "username": order.user.username,
            "product_name": order.product.name,
            "quantity": order.quantity,
            "ordered_at": order.ordered_at,
            "payment_status": order.payment_status,
            "payment_id": order.payment_id,
            "razorpay_order_id":order.razorpay_order_id
   })

    return result 
@router.get("/vendor/orders")
def get_vendor_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    orders = (
        db.query(Order)
        .join(Product, Order.product_id == Product.id)
        .filter(Product.vendor_id == current_user.id)
        .all()
    )

    result = []

    for order in orders:
        result.append({
           "order_id": order.id,

    "customer_id": order.user.id,
    "customer_name": order.user.username,
    "customer_email": order.user.email,

    "product_name": order.product.name,
    "product_price": order.product.price,
    "quantity": order.quantity,

    "ordered_at": order.ordered_at,

    "payment_status": order.payment_status,
    "razorpay_order_id": order.razorpay_order_id,
    "razorpay_payment_id": order.razorpay_payment_id
        })

    return result
@router.put("/{order_id}")
def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return {
        "message": "Order updated successfully",
        "order": order
    }
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }