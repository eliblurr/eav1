from sqlalchemy import Float, event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets

class PromoVouchers(Base):
    __tablename__ = "promo_vouchers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    promo_code = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    discount = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))

    is_active = Column(Boolean, default=True)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
