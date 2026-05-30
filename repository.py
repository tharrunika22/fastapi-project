from app.features.products.models import Product

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

    return product


def get_products(db):
    return db.query(Product).all()
