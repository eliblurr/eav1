from ..product_router.schemas import Product
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Form
import datetime

class CategoryImageBase(BaseModel):
    image_url: str
    category_id: int
    folder_name: Optional[str]

class CreateCategoryImage(CategoryImageBase):
    pass

class UpdateCategoryImage(BaseModel):
    image_url: Optional[str]
    category_id: Optional[int]
    folder_name: Optional[str]

class CategoryImage(CategoryImageBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True
    
class CategoryBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateCategory(CategoryBase):
    
    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(None), status: bool=Form(None)):
        return cls(title=title, metatitle=metatitle, description=description, status=status)
 
class UpdateCategory(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class Category(CategoryBase):
    id: int
    images: List[CategoryImage]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config():
        orm_mode = True
