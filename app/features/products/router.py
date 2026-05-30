from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.products.models import Product
from app.features.products.schemas import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])
@router.post("/")
def create_product(data: ProductCreate, db: Session = Depends(get_db)):

    new_product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product created successfully",
        "product": new_product
    }
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()
    return products
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "product": product
    }
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }