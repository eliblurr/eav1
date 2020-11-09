from pydantic import BaseModel
from typing import Optional, List

from fastapi import Form

import datetime

from ..product_router import schemas as product

class EventImages(BaseModel):
    image_url: str
    event_id: int
    id: int

class EventsBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreateEvents(EventsBase):
    # event_items_id: List[int]

    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(None) ):
        return cls(title=title, metatitle=metatitle, description=description)
 
 
class UpdateEvents(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]

class Events(EventsBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime
    images: List

    class Config():
        orm_mode = True
