from pydantic import BaseModel
from typing import Optional, List
import datetime

from ..product_router.schemas import  Product

class BoardBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]

class CreateBoard(BoardBase):
    board_items_id: List[int]
    # user_id: int

class UpdateBoard(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]

class Board(BoardBase):
    # id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True



class Board(BoardBase):
    date_created: datetime.datetime
    date_modified: datetime.datetime
    board_items: Product

    class Config():
        orm_mode = True

class BoardSummary(BoardBase):
    date_created: datetime.datetime
    date_modified: datetime.datetime
    # board_items: Optional[List[Product]]

    class Config:
        orm_mode = True


# id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     metatitle = Column(String, nullable=True)
#     description = Column(String, nullable=True)

#     user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
#     board_items = relationship('Products', secondary=board_items, backref='board', lazy='dynamic')

# class BoardResponse(BoardBase):
#     board_items: List[product.Product]
#     user_id: int
#     # board_items_id: List[int]
#     # user_id: int