from ..users_router.schemas import User
from pydantic import BaseModel
from typing import Optional
import datetime

class ReviewBase(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    ratings: float

class CreateReview(ReviewBase):
    pass

class UpdateReview(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    ratings: Optional[float]

class Review(ReviewBase):
    id: int
    product_id: int
    author: User
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True