from typing import Optional, List
from pydantic import BaseModel

class DeliveryBase(BaseModel):
    id: int
    title: int
    metatitle: Optional[int]
    description: Optional[int]
    duration: int
    price: float
    status: bool

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    title: Optional[int]
    metatitle: Optional[int]
    description: Optional[int]
    duration: Optional[int]
    price: Optional[float]
    status: Optional[bool]

class Delivery(DeliveryBase):
    pass

    class Config:
        orm_mode=True
