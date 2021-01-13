from pydantic import BaseModel
from typing import Optional
import datetime

class CountryBase(BaseModel):
    name: str

class CreateCountry(CountryBase):
    currency_id: int

class UpdateCountry(BaseModel):
    name: Optional[str]
    currency_id: Optional[int]

class Country(CountryBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class SubCountryBase(BaseModel):
    name: str

class CreateSubCountry(SubCountryBase):
    country_id: int

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
    geo_name_id: int
    status: Optional[bool]
    
class CreateLocation(LocationBase):
    sub_country_id: int

class UpdateLocation(BaseModel):
    name: Optional[str]
    geo_name_id: Optional[int]
    status: Optional[bool]

class Location(LocationBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True