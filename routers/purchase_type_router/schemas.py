from typing import Optional, List
from pydantic import BaseModel
import datetime

class PurchaseTypeBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreatePurchaseType(PurchaseTypeBase):
    status: Optional[bool]

class UpdatePurchaseType(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class PurchaseType(PurchaseTypeBase):
    status: Optional[bool]
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True