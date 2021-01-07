from ..timeline_router.schemas import Timeline
from typing import Optional, List
from pydantic import BaseModel, validator
import datetime

class DeliveryOptionBase(BaseModel):
    title: str
    rate: float
    min_duration: int
    max_duration: Optional[int]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

    @validator('max_duration')
    def duration_validation(cls, value, values):
        if value and value < values['min_duration']:
            raise ValueError("max duration can't be less than min duration")
        return value

class CreateDeliveryOption(DeliveryOptionBase):
    location_ids: List[int] = []

class UpdateDeliveryOption(BaseModel):
    title: Optional[str]
    rate: Optional[float]
    max_duration: Optional[int]
    min_duration: Optional[int]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class DeliveryOption(DeliveryOptionBase):
    id: int
    price_to_pay: float
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

#///////////////////////////////////

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

class DeliveryBase(BaseModel):
    status: Optional[bool]
    delivery_option_id: int
    price: float
    order_id: int

class CreateDelivery(DeliveryBase):
    pass

class UpdateDelivery(BaseModel):
    status: Optional[bool]
    delivery_option_id: Optional[int]
    price: Optional[float]

class Delivery(DeliveryBase):
    id: int
    delivery_option: DeliveryOption
    delivery_timeline: List[DeliveryTimeline]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class AddressBase(BaseModel):
    country_id: int
    sub_country_id: int 
    location_id: Optional[int]
    zip_code: str

class Address(AddressBase):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    address_line_1: str
    address_line_2: str
