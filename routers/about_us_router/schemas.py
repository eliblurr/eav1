from pydantic import BaseModel
from typing import Optional
import datetime

class AboutUsBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str
    index: int
    status: Optional[bool]

class CreateAboutUs(AboutUsBase):
    pass

class UpdateAboutUs(AboutUsBase):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    index: Optional[int]
    status: Optional[bool]

class AboutUs(AboutUsBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True