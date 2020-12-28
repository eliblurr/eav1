from pydantic import BaseModel
from typing import Optional
import datetime

class WeightUnitBase(BaseModel):
    title: str
    symbol: str
    status: Optional[bool]

class CreateWeightUnit(WeightUnitBase):
    pass

class UpdateWeightUnit(BaseModel):
    title: Optional[str]
    symbol: Optional[str]
    status: Optional[bool]

class WeightUnit(WeightUnitBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True