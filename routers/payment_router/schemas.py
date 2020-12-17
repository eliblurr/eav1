from pydantic import BaseModel
from typing import Optional
import datetime

from ..payment_type_router.schemas import PaymentType

class PaymentBase(BaseModel):
    amount: float
    comment: Optional[str]

class CreatePayment(PaymentBase):
    status: Optional[bool]
    payment_type_id: Optional[int]

class UpdatePayment(BaseModel):
    payment_type_id: Optional[int]
    amount: Optional[float]
    comment: Optional[str]
    status: Optional[bool]

class Payment(PaymentBase):
    id: int
    status: bool
    created_date: datetime.datetime
    updated_date: datetime.datetime
    payment_type: Optional[PaymentType]

    class Config:
        orm_mode = True