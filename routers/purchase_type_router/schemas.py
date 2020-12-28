from typing import Optional, List
from pydantic import BaseModel
import datetime

class PurchaseTypeBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreatePurchaseType(PurchaseTypeBase):
    pass

class UpdatePurchaseType(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class PurchaseType(PurchaseTypeBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True