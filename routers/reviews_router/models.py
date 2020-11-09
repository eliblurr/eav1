from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, DateTime, Float
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    ratings = Column(Float, nullable=False)

    author = relationship('UserInfo')
    user_id = Column(Integer, ForeignKey("user_info.user_id"), nullable=True )

    product_id = Column(Integer, ForeignKey("products.id"), nullable=True )

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

