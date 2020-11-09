from pydantic import BaseModel
from typing import Optional, List

class AnnouncementBase(BaseModel):
    description: str
    is_active: bool

class CreateAnnouncement(AnnouncementBase):
    pass

class UpdateAnnouncement(BaseModel):
    description: Optional[str]
    is_active: Optional[bool]

class Announcement(AnnouncementBase):
    id: int

    class Config():
        orm_mode = True