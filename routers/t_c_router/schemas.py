from pydantic import BaseModel
from typing import Optional, List

class TCBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str
    

class CreateTC(TCBase):
    index : int

class UpdateTC(TCBase):
    index : Optional[int]

class TC(TCBase):
    id: int
    index : int
    
    class Config():
        orm_mode = True