from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets

# from ..promo_router.models import PromoVouchers

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # order_type
    # order_products
    # order_status

class OrderType(Base):
    __tablename__ = "order_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)

# trigger
@event.listens_for(OrderType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([
        OrderType(title='rental'),
        OrderType(title='purchase')
    ])
    db.commit()

