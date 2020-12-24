from ..product_router.schemas import Product
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Form
import datetime

class EventImageBase(BaseModel):
    image_url: str
    event_id: int
    folder_name: Optional[str]

class CreateEventImage(EventImageBase):
    pass

class UpdateEventImage(BaseModel):
    image_url: Optional[str]
    event_id: Optional[int]
    folder_name: Optional[str]

class EventImage(EventImageBase):
    id: int

    class Config:
        orm_mode=True

class EventBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreateEvent(EventBase):

    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(None) ):
        return cls(title=title, metatitle=metatitle, description=description)

class UpdateEvent(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]

class Event(EventBase):
    id: int
    images: List[EventImage]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True

class EventItems(BaseModel):
    event_items: List[Product]

    class Config():
        orm_mode = True