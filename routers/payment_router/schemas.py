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
    comment: Optional[str]
    status: Optional[bool]

class CreatePayment(PaymentBase):     
    card: Optional[Card]
    payment_type_id: int

class UpdatePayment(BaseModel):
    amount: Optional[float]
    card: Optional[Card]
    comment: Optional[str]
    status: Optional[bool]
    payment_type_id: Optional[int]

class Payment(PaymentBase):
    id: int
    card_number_brand: str
    card_number_masked: str
    date_created: datetime.datetime
    date_modified: datetime.datetime
    
    class Config:
        orm_mode=True
