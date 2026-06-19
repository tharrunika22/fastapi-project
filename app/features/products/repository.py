from app.features.products.models import Product
from app.features.products.product_image_model import ProductImage

def create_product(db, product_data):
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock
    ) 

    db.add(product)
    db.commit()
    db.refresh(product) 
    for url in product_data.image_urls:

        image = ProductImage(
            product_id=product.id,
            image_url=url
        )

        db.add(image)

    db.commit()

    return product


def get_products(db):
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