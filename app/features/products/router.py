from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.products.models import Product
from app.features.products.schemas import ProductCreate, ProductUpdate 
from app.core.security import get_current_user 
from app.features.users.models import User 
from app.features.products.product_image_model import ProductImage

router = APIRouter(prefix="/products", tags=["Products"])
@router.post("/")
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        vendor_id=current_user.id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # Save image URLs
    for url in data.image_urls:

        image = ProductImage(
            product_id=new_product.id,
            image_url=url
        )

        db.add(image)

    db.commit()

    return {
        "message": "Product created successfully",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "images": data.image_urls
        }
    }
@router.get("/vendor/products")
def get_vendor_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = (
        db.query(Product)
        .filter(Product.vendor_id == current_user.id)
        .all()
    )

    result = []

    for product in products:

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "images": [
                image.image_url
                for image in product.images
            ]
        })

    return result

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    result = []

    for product in products:

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "images": [
                image.image_url
                for image in product.images
            ]
        })

    return result
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "vendor_id": product.vendor_id,
        "images": [
            image.image_url
            for image in product.images
        ]
    }
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