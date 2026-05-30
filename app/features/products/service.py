from app.features.products import repository

def add_product(db, product_data):
    return repository.create_product(db, product_data)

def list_products(db):
    return repository.get_products(db)