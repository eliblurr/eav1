from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from database import Base, SessionLocal
from sqlalchemy.orm import relationship
import datetime

class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    priority_id = Column(Integer, ForeignKey("priorities.id"), nullable=True )
    subscription_type_id = Column(Integer, ForeignKey("subscription_type.id"), nullable=True)
    
class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    duration = Column(Integer, nullable=False)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    subscriptions = relationship('Subscriptions', backref="subscription_type", uselist=True, lazy="dynamic")
    
@event.listens_for(SubscriptionType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ SubscriptionType(title='one_time'), SubscriptionType(title='periodic') ])
    db.commit()


