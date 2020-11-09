from pydantic import BaseModel
from typing import Optional

import datetime

class PriorityBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    priority : int

class PriorityCreate(PriorityBase):
    pass

class PriorityUpdate(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    priority : Optional[int]

class Priority(PriorityBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True
