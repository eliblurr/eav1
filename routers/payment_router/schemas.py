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

from datetime import date

from pydantic import BaseModel
from pydantic.types import PaymentCardBrand, PaymentCardNumber, constr


class Card(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    number: PaymentCardNumber
    exp: date

    @property
    def brand(self) -> PaymentCardBrand:
        return self.number.brand

    @property
    def expired(self) -> bool:
        return self.exp < date.today()


card = Card(
    name='Georg Wilhelm Friedrich Hegel',
    number='4000000000000002',
    exp=date(2023, 9, 30),
)

assert card.number.brand == PaymentCardBrand.visa
assert card.number.bin == '400000'
assert card.number.last4 == '0002'
assert card.number.masked == '400000******0002'