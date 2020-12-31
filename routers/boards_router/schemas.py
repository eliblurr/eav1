from ..product_router.schemas import Product
from typing import Optional, List
from pydantic import BaseModel
import datetime

class BoardBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateBoard(BoardBase):
    user_id: int
    product_ids: Optional[List[int]]

class UpdateBoard(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class Board(BoardBase):
    id: int
    user_id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True