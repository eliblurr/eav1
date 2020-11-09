from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets

class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=True, default=None)

    priority_id = Column(Integer, ForeignKey("priorities.id"), nullable=True )
    subscription_type_id = Column(Integer, ForeignKey("subscription_type.id"), nullable=True)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    

class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)

    subscriptions = relationship('Subscriptions', backref="subscription_type", uselist=True)



@event.listens_for(SubscriptionType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([
        SubscriptionType(title='one_time'),
        SubscriptionType(title='periodic')
    ])
    db.commit()


