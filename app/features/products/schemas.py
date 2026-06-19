from pydantic import BaseModel
from typing import Optional 
from typing import List


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int 
    image_urls: List[str]



class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None