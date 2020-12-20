from typing import List, Optional
from pydantic import BaseModel

from ..reviews_router.schemas import Reviews

import datetime

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    quantity: int
    status: bool
    date_modified: datetime.datetime
    purchase_type_id: int
    # purchase: bool
    date_created: datetime.datetime
    # rental: bool
    quantity: int
     
class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    # pass
    id: int
    reviews: List[Reviews]

    class Config:
        orm_mode = True





