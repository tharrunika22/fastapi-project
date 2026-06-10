from app.features.cart.models import Cart


def create_cart_item(db, cart):
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_cart_by_user(db, user_id):
    return db.query(Cart).filter(
        Cart.user_id == user_id
    ).all()


def get_cart_item(db, cart_id):
    return db.query(Cart).filter(
        Cart.id == cart_id
    ).first()


def delete_cart_item(db, cart_item):
    db.delete(cart_item)
    db.commit()