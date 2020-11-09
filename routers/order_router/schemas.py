from pydantic import BaseModel
from typing import Optional, List

from ..product_router import schemas as product

class RentalBase(BaseModel):
    quantity: int
    duration: int
    product_id: int

class Rental(RentalBase):
    pass

class PurchaseBase(BaseModel):
    quantity: int
    duration: int

class Purchase(PurchaseBase):
    pass