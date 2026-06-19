from .models import Address


def create_address(db, user_id, data):
    address = Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        address_line=data.address_line,
        city=data.city,
        state=data.state,
        pincode=data.pincode,
    )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address 
def get_addresses(db, user_id):
    return (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .all()
    )
def delete_address(db, address_id, user_id):
    address = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == user_id)
        .first()
    )

    if address:
        db.delete(address)
        db.commit()
        return True
    return False 
def update_address(db, address_id, user_id, data):
    address = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == user_id)
        .first()
    )

    if not address:
        return None

    address.full_name = data.full_name
    address.phone = data.phone
    address.address_line = data.address_line
    address.city = data.city
    address.state = data.state
    address.pincode = data.pincode

    db.commit()
    db.refresh(address)

    return address