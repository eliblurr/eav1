from typing import Optional, List
from pydantic import BaseModel
import datetime

class AnnouncementBase(BaseModel):
    description: str
    status: Optional[bool]

class CreateAnnouncement(AnnouncementBase):
    pass

class UpdateAnnouncement(BaseModel):
    description: Optional[str]
    status: Optional[bool]

class Announcement(AnnouncementBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True