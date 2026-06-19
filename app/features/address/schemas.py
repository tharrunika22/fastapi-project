from pydantic import BaseModel

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pincode: str


class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True