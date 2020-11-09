from pydantic import BaseModel
from typing import Optional, List

class AboutUsBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: str

class CreateAboutUs(AboutUsBase):
    index: int

class UpdateAboutUs(AboutUsBase):
    description: Optional[str]
    index: Optional[int]
    pass

class AboutUs(AboutUsBase):
    id: int
    index: int

    class Config():
        orm_mode = True