from pydantic import BaseModel
from typing import Optional, List

from fastapi import Form

import datetime

from ..product_router.schemas import Product

class CategoryImages(BaseModel):
    image_url: str
    category_id: int
    id: int

class CategoryBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreateCategory(CategoryBase):

    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(None) ):
        return cls(title=title, metatitle=metatitle, description=description)
 
class UpdateCategory(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]

class Category(CategoryBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime
    images: List

    class Config():
        orm_mode = True

class CategoryItems(CategoryBase):
    category_items: Product

    class Config():
        orm_mode = True
