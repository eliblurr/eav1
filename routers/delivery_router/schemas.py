from typing import Optional, List
from pydantic import BaseModel

class DeliveryBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    duration: int
    price: float
    status: bool

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    duration: Optional[int]
    price: Optional[float]
    status: Optional[bool]

class Delivery(DeliveryBase):
    id: int

    class Config:
        orm_mode=True
