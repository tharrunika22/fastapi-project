from app.features.address.repository import (
    create_address as repo_create,
    get_addresses,
    update_address as repo_update,
    delete_address as repo_delete,
)


def create_address(db, user_id, data):
    return repo_create(
        db=db,
        user_id=user_id,
        data=data
    )


def get_user_addresses(db, user_id):
    return get_addresses(
        db=db,
        user_id=user_id
    )


def update_address(db, address_id, user_id, data):
    return repo_update(
        db=db,
        address_id=address_id,
        user_id=user_id,
        data=data
    )


def delete_address(db, address_id, user_id):
    return repo_delete(
        db=db,
        address_id=address_id,
        user_id=user_id
    )