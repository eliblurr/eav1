from pydantic import BaseModel
from typing import Optional, List

class PoliciesBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str
    

class CreatePolicies(PoliciesBase):
    index : int

class UpdatePolicies(PoliciesBase):
    index : Optional[int]

class Policies(PoliciesBase):
    id: int
    index : int

    class Config():
        orm_mode = True
