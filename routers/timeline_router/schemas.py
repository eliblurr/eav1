from pydantic import BaseModel
from typing import Optional
import datetime

class TimelineBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreateTimeline(TimelineBase):
    status: Optional[bool]

class UpdateTimeline(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class Timeline(TimelineBase):
    status: bool
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True