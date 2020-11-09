from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship, backref

import datetime

from database import Base, metadata, engine

from ..product_router.models import Products

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)

    images = relationship('EventImages', backref="event", uselist=True, cascade="all, delete")

    event_items = relationship('Products', secondary='event_items', backref=backref('events', lazy='dynamic'), lazy='dynamic')

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class EventItems(Base):
    __tablename__ = 'event_items'

    event_id = Column(Integer, ForeignKey('events.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)


class EventImages(Base):
    __tablename__ = "event_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    event_id = Column(Integer, ForeignKey('events.id'))
    image_url = Column(String, nullable=True)