from pydantic import BaseModel
from typing import Optional
import datetime

class TimelineBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateTimeline(TimelineBase):
    pass

class UpdateTimeline(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class Timeline(TimelineBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True