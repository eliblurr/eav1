from pydantic import BaseModel
from typing import Optional, List

class LocationBase(BaseModel):
    name: str
    country: str
    sub_country: str
    geo_name_id: int

class CreateLocation(BaseModel):
    name: str
    country: str
    sub_country: str
    geo_name_id: Optional[int]

class UpdateLocation(BaseModel):
    name: Optional[str]
    country: Optional[str]
    sub_country: Optional[str]
    geo_name_id: Optional[int]

class Location(LocationBase):
    id: int

    class Config():
        orm_mode = True

# {
#     "sub_country": "Central",
#     "name": "Winneba",
#     "id": 2,
#     "geo_name_id": 2294034,
#     "country": "Ghana"
#   }
