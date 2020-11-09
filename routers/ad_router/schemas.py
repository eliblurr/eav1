from pydantic import BaseModel
from typing import Optional

class AdsBase(BaseModel):
    title: str
    metatitle: str
    description: str
    image_url: str
    component_id: int
    ad_style: int
    priority: int

class AdsCreate(AdsBase):
    pass

class AdsUpdate(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    component_id: Optional[int]
    ad_style: Optional[int]
    priority: Optional[int]

class Ads(AdsBase):
    pass