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

# id = Column(Integer, primary_key=True, index=True, autoincrement=True)
# title = Column(String, nullable=False)
# metatitle = Column(String, nullable=True)
# description = Column(String, nullable=True)
# rate = Column(Float, nullable=False, default=0) 
# max_duration = Column(Integer, nullable=True)
# min_duration = Column(Integer, nullable=False)
# status = Column(Boolean, default=True, nullable=False)
# date_created = Column(DateTime, default=datetime.datetime.utcnow)
# date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
# deliveries = relationship('Delivery', backref='delivery_option', uselist=True, lazy="dynamic")
# price_to_pay = 0

# ///////////

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

class DeliveryBase(BaseModel):
    price: float
    status: Optional[bool]
    order_id: Optional[int]
    delivery_address: CreateDeliveryAddress
    
class CreateDelivery(DeliveryBase):
    delivery_option_id: int

class UpdateDelivery(BaseModel):
    status: Optional[bool]
    price: Optional[float]
    price: Optional[float]

class CreateDeliveryTimeline(BaseModel):
    index: int
    timeline_id: int
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

    @validator('timeline_id')
    def timeline_validation(cls, v, values, **kwargs):
        if not v:
            raise ValueError('timeline_id cannot be empty or 0')
        return v
    
    @validator('index')
    def index_validation(cls, v):
        if not v:
            raise ValueError("index cannot be null or 0")
        return v

#///////////////////////////////////

class DeliveryTimeline(BaseModel):
    index: int
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    date_created: datetime.datetime
    date_modified: datetime.datetime
    timeline: Timeline
    delivery_id: int

    class Config:
        orm_mode=True

class Delivery(DeliveryBase):
    id: int
    delivery_option: DeliveryOption
    delivery_address: DeliveryAddress
    # delivery_timeline: List[DeliveryTimeline]
    # delivery_timeline: Optional[List[DeliveryTimeline]]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

  # delivery_id = Column(Integer, ForeignKey("delivery.id"), primary_key=True)
    #  timeline_id = Column(Integer, ForeignKey("timeline.id"), primary_key=True)
    #  index = Column(Integer, nullable=False,  primary_key=True)
    #  title = Column(String, nullable=True)
    #  metatitle = Column(String, nullable=True)
    #  description = Column(String, nullable=True)
    #  status = Column(Boolean, default=True, nullable=True)
    #  date_created = Column(DateTime, default=datetime.datetime.utcnow)
    #  date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    #  timeline = relationship("Timeline", back_populates="delivery")
    #  delivery
