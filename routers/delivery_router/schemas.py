from ..timeline_router.schemas import Timeline
from typing import Optional, List
from pydantic import BaseModel
import datetime

class DeliveryOptionBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateDeliveryOption(DeliveryOptionBase):
    pass

class UpdateDeliveryOption(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class DeliveryOption(DeliveryOptionBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class DeliveryBase(BaseModel):
    pass

class CreateDelivery(DeliveryBase):
    pass

class UpdateDelivery(BaseModel):
    pass

class Delivery(DeliveryBase):
    pass

    class Config:
        orm_mode=True

class CreateDeliveryTimeline(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    index: int

class DeliveryTimeline(BaseModel):
    id: Optional[int]
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    date_created: datetime.datetime
    date_modified: datetime.datetime
    delivery_timeline: Optional[Timeline]

    class Config:
        orm_mode=True