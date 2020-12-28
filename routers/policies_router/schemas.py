from pydantic import BaseModel
from typing import Optional
import datetime

class PoliciesBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str
    index: int
    status: Optional[bool]
    
class CreatePolicies(PoliciesBase):
    pass

class UpdatePolicies(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    index: Optional[int]
    status: Optional[bool]

class Policies(PoliciesBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True
