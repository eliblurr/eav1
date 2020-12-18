from typing import Optional, List
from pydantic import BaseModel

from ..product_router import schemas as product

class OrderBase(BaseModel):
    pass

class CreateOrder(OrderBase):
    pass

class UpdateOrder(BaseModel):
    pass

class Order(OrderBase):
    pass