from pydantic import BaseModel
from typing import Optional, List

class FAQsBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]

class CreateFAQs(FAQsBase):
    index: int

class UpdateFAQs(FAQsBase):
    index: int

class FAQs(FAQsBase):
    id: int
    index: int

    class Config():
        orm_mode = True