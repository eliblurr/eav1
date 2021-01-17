from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Float, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, backref
from ..timeline_router.models import Timeline
from ..location_router.models import Location
from database import Base
import datetime

class Delivery(Base):
     __tablename__ = "delivery"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     price = Column(Float, nullable=False) #changeable based on delivery distance and time
     status = Column(Boolean, default=True, nullable=False)
     order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
     delivery_option_id = Column(Integer, ForeignKey("delivery_options.id"), nullable=False)
     delivery_address = relationship('DeliveryAddress', uselist=False, backref="delivery", cascade="all, delete")
     timeline = relationship('DeliveryTimeline', back_populates='delivery', cascade="all, delete")
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
     
class DeliveryAddress(Base):
     __tablename__ = "delivery_address"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     first_name = Column(String, nullable=False)
     middle_name = Column(String, nullable=True)
     last_name = Column(String, nullable=False)
     phone = Column(String, nullable=False)
     address_line_1 = Column(String, nullable=False)
     address_line_2 = Column(String, nullable=True)
     status = Column(Boolean, default=True, nullable=False)
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
     delivery_id = Column(Integer, ForeignKey("delivery.id"), nullable=False)
     location_id = Column(Integer, ForeignKey('locations.id'))
     location = relationship('Location')
     
class DeliveryOption(Base):
     __tablename__ = "delivery_options"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     title = Column(String, nullable=False)
     metatitle = Column(String, nullable=True)
     description = Column(String, nullable=True)
     rate = Column(Float, nullable=False, default=0) #price per kilogram
     max_duration = Column(Integer, nullable=True)
     min_duration = Column(Integer, nullable=False)
     status = Column(Boolean, default=True, nullable=False)
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
     deliveries = relationship('Delivery', backref='delivery_option', uselist=True, lazy="dynamic")
     price_to_pay = 0

class DeliveryTimeline(Base):
     __tablename__ = "delivery_timeline"
     __table_args__ = (
          UniqueConstraint('delivery_id', 'timeline_id', 'title', 'index', name='_delivery_timeline_dtti'),
          UniqueConstraint('delivery_id', 'timeline_id', 'title', name='_delivery_timeline_dtt'),
          UniqueConstraint('delivery_id', 'timeline_id', 'index', name='_delivery_timeline_dti'),
          UniqueConstraint('delivery_id', 'index', name='_delivery_timeline_di'),
          UniqueConstraint('delivery_id', 'title', name='_delivery_timeline_dt'),
          CheckConstraint('coalesce(timeline_id , title ) is not null'),
     )

     delivery_id = Column(Integer, ForeignKey("delivery.id"), primary_key=True)
     timeline_id = Column(Integer, ForeignKey("timeline.id"), primary_key=True)
     index = Column(Integer, nullable=False,  primary_key=True)
     title = Column(String, nullable=True)
     metatitle = Column(String, nullable=True)
     description = Column(String, nullable=True)
     status = Column(Boolean, default=True, nullable=True)
     date_created = Column(DateTime, default=datetime.datetime.utcnow)
     date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
     timeline = relationship("Timeline", back_populates="delivery")
     delivery = relationship("Delivery", back_populates="timeline")