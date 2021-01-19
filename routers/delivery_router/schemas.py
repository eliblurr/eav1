from ..timeline_router.schemas import Timeline
from ..location_router.schemas import Location
from pydantic import BaseModel, validator
from typing import Optional, List
import datetime

class DeliveryOptionBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    rate: float
    min_duration: int
    max_duration: Optional[int]
    status: Optional[bool]

    @validator('max_duration')
    def duration_validation(cls, value, values):
        if value and value < values['min_duration']:
            raise ValueError("max duration can't be less than min duration")
        return value

class CreateDeliveryOption(DeliveryOptionBase):
    location_ids: List[int]

class UpdateDeliveryOption(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    rate: Optional[float]
    max_duration: Optional[int]
    min_duration: Optional[int]
    status: Optional[bool]

class DeliveryOption(DeliveryOptionBase):
    id: int
    price_to_pay: float
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class DeliveryAddressBase(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    phone: str
    address_line_1: str
    address_line_2: Optional[str]
    status: Optional[bool]

class CreateDeliveryAddress(DeliveryAddressBase):
    location_id: int

class UpdateDeliveryAddress(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    status: Optional[bool]

class DeliveryAddress(DeliveryAddressBase):
    id: int
    location: Location
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class CreateDeliveryTimeline(BaseModel):
    index: int
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    timeline_id: Optional[int]
    
    @validator('index')
    def index_validation(cls, index):
        if not index:
            raise ValueError("index cannot be null or 0")
        return index
    
    @validator('timeline_id')
    def not_null(cls, timeline_id, values):
        if not (timeline_id or values['title']):
            raise ValueError("both timeline_id and title cannot be None")
        return timeline_id

class DeliveryTimeline(BaseModel):
    index: int
    delivery_id: int
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    date_created: datetime.datetime
    date_modified: datetime.datetime
    timeline: Optional[Timeline]
    
    class Config:
        orm_mode=True

class DeliveryBase(BaseModel):
    price: float
    status: Optional[bool]
    order_id: Optional[int]

class CreateDelivery(DeliveryBase):
    delivery_option_id: int
    delivery_address: CreateDeliveryAddress

class UpdateDelivery(BaseModel):
    status: Optional[bool]
    price: Optional[float]

class Delivery(DeliveryBase):
    id: int
    delivery_option: DeliveryOption
    delivery_address: DeliveryAddress
    delivery_timeline: List[DeliveryTimeline]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True
