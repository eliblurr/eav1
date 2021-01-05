from ..product_router import schemas as product
from typing import Optional, List
from pydantic import BaseModel
import datetime

class OrderStateBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateOrderState(OrderStateBase):
    pass

class UpdateOrderState(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class OrderState(OrderStateBase):
    id:int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class OrderBase(BaseModel):
    pass

class CreateOrder(OrderBase):
    pass

class UpdateOrder(BaseModel):
    pass

class Order(OrderBase):
    pass
