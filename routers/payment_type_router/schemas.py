from pydantic import BaseModel
from typing import Optional
import datetime

class PaymentTypeBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreatePaymentType(PaymentTypeBase):
    pass

class UpdatePaymentType(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[int]

class PaymentType(PaymentTypeBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True