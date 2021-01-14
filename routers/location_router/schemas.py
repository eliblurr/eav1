from ..weight_unit_router.schemas import WeightUnit
from ..currency_router.schemas import Currency
from pydantic import BaseModel, conint
from typing import Optional
import datetime

class CountryBase(BaseModel):
    name: str

class CreateCountry(CountryBase):
    currency_id: conint(gt=0)
    weight_unit_id: conint(gt=0)

class UpdateCountry(BaseModel):
    name: Optional[str]
    currency_id: Optional[conint(gt=0)]
    weight_unit_id: Optional[conint(gt=0)]

class Country(CountryBase):
    id: int
    currency: Currency
    weight_unit: WeightUnit
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class SubCountryBase(BaseModel):
    name: str

class CreateSubCountry(SubCountryBase):
    country_id: conint(gt=0)

class UpdateSubCountry(BaseModel):
    name: Optional[str]

class SubCountry(CreateSubCountry):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    name: str
    geo_name_id: conint(gt=0)
    status: Optional[bool]
    
class CreateLocation(LocationBase):
    sub_country_id: conint(gt=0)

class UpdateLocation(BaseModel):
    name: Optional[str]
    geo_name_id: Optional[conint(gt=0)]
    status: Optional[bool]

class Location(LocationBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True