from pydantic import BaseModel, color
from typing import Optional, List
from fastapi import Form
import datetime

class StylesBase(BaseModel):
    background_color: Optional[color.Color]
    text_color: Optional[color.Color]
    fontWeight: Optional[int]
    status:Optional[bool]

class CreateStyle(StylesBase):
    pass

class UpdateStyle(StylesBase):
    pass

class Style(StylesBase):
    id:int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class AdImageBase(BaseModel):
    image_url: str
    category_id: int
    folder_name: Optional[str]

class CreateAdImage(AdImageBase):
    pass

class UpdateAdImage(BaseModel):
    image_url: Optional[str]
    category_id: Optional[int]
    folder_name: Optional[str]

class AdImage(AdImageBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class AdBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateAd(BaseModel):
    style_id:Optional[int]
    location_ids:List[int]

    @classmethod
    def as_form(cls, title: str = Form(None), metatitle: str = Form(None), description: str = Form(None), status: bool=Form(None), style_id:int=Form(None), location_ids:List[int]=Form([])):
        return cls(title=title, metatitle=metatitle, description=description, status=status, style_id=style_id, location_ids=location_ids)

class UpdateAd(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    component_id: Optional[int]
    ad_style: Optional[int]
    priority: Optional[int]

class Ad(AdBase):
    id: int
    # style: 
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True