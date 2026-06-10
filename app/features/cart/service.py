from app.features.cart.models import Cart
from app.features.cart.repository import (
    create_cart_item,
    get_cart_by_user,
    get_cart_item,
    delete_cart_item
)


def add_to_cart(db, user_id, data):

    cart_item = Cart(
        user_id=user_id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    return create_cart_item(
        db,
        cart_item
    )


def get_user_cart(db, user_id):
    return get_cart_by_user(
        db,
        user_id
    )


def remove_from_cart(db, cart_id):

    cart_item = get_cart_item(
        db,
        cart_id
    )

    if not cart_item:
        return None

    delete_cart_item(
        db,
        cart_item
    )

    return True