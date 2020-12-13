from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from . import models
import datetime
import secrets

# from ..promo_router.models import PromoVouchers
# from ..users_router.models import User
# from ..deliveries_router.models import Delivery

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Boolean)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

class PurchaseType(Base):
    __tablename__ = "purchase_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

# trigger
@event.listens_for(PurchaseType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([
        PurchaseType(title='rental', status=True),
        PurchaseType(title='purchase', status=True)
    ])
    db.commit()

