from pydantic.types import PaymentCardBrand, PaymentCardNumber, constr
from ..payment_type_router.schemas import PaymentType
from pydantic import BaseModel
from typing import Optional
import datetime

class Card(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    number: PaymentCardNumber
    exp: datetime.date

    @property
    def brand(self) -> PaymentCardBrand:
        return self.number.brand

    @property
    def expired(self) -> bool:
        return self.exp < datetime.date.today()

class PaymentBase(BaseModel):
    amount: float
    card: Optional[Card]
    comment: Optional[str]
    status: Optional[bool]
    payment_type_id: int

class CreatePayment(PaymentBase):     
    pass

class UpdatePayment(BaseModel):
    amount: Optional[float]
    card: Optional[Card]
    comment: Optional[str]
    status: Optional[bool]
    payment_type_id: Optional[int]

class Payment(PaymentBase):
    id: int
    payment_type: PaymentType
    date_created: datetime.datetime
    date_modified: datetime.datetime
    
    class Config:
        orm_mode=True
