from pydantic import BaseModel
from typing import Optional
import datetime

class PaymentTypeBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreatePaymentType(PaymentTypeBase):
    status: Optional[int]

class UpdatePaymentType(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[int]

class PaymentType(PaymentTypeBase):
    id: int
    status: bool
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True
