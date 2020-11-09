from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship, backref


import datetime

from database import Base, metadata, engine

# from ..product_router.models import Products

class TC(Base):
    __tablename__ = "t_c"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)

    index = Column(Integer, autoincrement=True, nullable=False, unique=True, index=True)

