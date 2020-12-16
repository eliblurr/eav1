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
    status = Column(Boolean, default=True)
    order_timeline = relationship('OrderTimeline', backref="order", uselist=True, cascade="all, delete",lazy='dynamic')

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

class OrderTimeline(Base):
    __tablename__ = "order_timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    status = Column(Boolean, default=True)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    timeline_id = Column(Integer, ForeignKey("timeline.id"), nullable=True)

    # relationships
    # orders = relationship('Orders', backref="order_timeline", uselist=True, cascade="all, delete", lazy='dynamic')
    # reviews = relationship('Reviews', backref="product", uselist=True, cascade="all, delete",lazy='dynamic')
    # product_id = Column(Integer, ForeignKey("products.id"), nullable=True )
    
    # custom order timeline
