from pydantic import BaseModel
from typing import Optional
import datetime

class TCBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str
    index: int
    status: Optional[bool]

class CreateTC(TCBase):
    pass

class UpdateTC(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    index: Optional[int]
    status: Optional[bool]

class TC(TCBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime
    
    class Config():
        orm_mode = True