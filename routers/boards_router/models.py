from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from ..product_router.models import Products
from database import Base
import datetime

class Boards(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    board_items = relationship('Products', secondary='board_items', backref=backref('board', lazy='dynamic'), lazy='dynamic')
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class BoardItems(Base):
    __tablename__ = 'board_items'

    board_id = Column(Integer, ForeignKey('boards.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)