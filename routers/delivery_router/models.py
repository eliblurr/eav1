from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship, backref
from ..timeline_router.models import Timeline
from database import Base
import datetime

class Delivery(Base):
     __tablename__ = "delivery"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     price = Column(Float, nullable=False) #changeable based on delivery distance and time
     status = Column(Boolean, default=True, nullable=False)
     order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
     delivery_option_id = Column(Integer, ForeignKey("delivery_options.id"), nullable=False)
     delivery_timeline = relationship('Timeline', secondary='delivery_timeline', backref=backref('delivery', lazy='dynamic'), cascade="all, delete", lazy="dynamic")
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DeliveryTimeline(Base):
     __tablename__ = "delivery_timeline"

     delivery_id = Column(Integer, ForeignKey("delivery.id"), nullable=False, primary_key=True)
     timeline_id = Column(Integer, ForeignKey("timeline.id"), nullable=True)
     index = Column(Integer, nullable=False)
     title = Column(String, nullable=True)
     metatitle = Column(String, nullable=True)
     description = Column(String, nullable=True)
     status = Column(Boolean, default=True, nullable=True)
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
 
class DeliveryOption(Base):
     __tablename__ = "delivery_options"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     title = Column(String, nullable=False)
     metatitle = Column(String, nullable=True)
     description = Column(String, nullable=True)
     duration = Column(Integer, nullable=False)
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
     deliveries = relationship('Delivery', backref='delivery_option', uselist=True, lazy="dynamic")