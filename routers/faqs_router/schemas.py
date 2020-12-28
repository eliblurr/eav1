from pydantic import BaseModel
from typing import Optional
import datetime

class FAQsBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: str
    index: int
    status: Optional[bool]

class CreateFAQs(FAQsBase):
    pass

class UpdateFAQs(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    index: Optional[int]

class FAQs(FAQsBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True