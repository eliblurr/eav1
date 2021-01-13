from pydantic import BaseModel
from typing import Optional
import datetime

class CurrencyBase(BaseModel):
    title: str
    symbol: Optional[str]
    status: Optional[bool]

class CreateCurrency(CurrencyBase):
    pass

class UpdateCurrency(BaseModel):
    title: Optional[str]
    symbol: Optional[str]
    status: Optional[bool]

class Currency(CurrencyBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True