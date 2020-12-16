from typing import List, Optional
from pydantic import BaseModel

import datetime

from ..users_router.schemas import User

class ReviewsBase(BaseModel):
    title: str
    metatitle: Optional[str] = None
    description: Optional[str] = None
    ratings: float


class ReviewsCreate(ReviewsBase):
    pass

class ReviewsUpdate(BaseModel):
    title: Optional[str] = None
    metatitle: Optional[str]  = None
    description: Optional[str] = None
    ratings: Optional[float] = None

class Reviews(ReviewsBase):
    id: int
    product_id: int
    date_modified: datetime.datetime
    date_created: datetime.datetime

    author: User

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

   