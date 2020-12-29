from sqlalchemy import Boolean, Column, Integer, String, DateTime
from ..subscriptions_router.models import Subscriptions
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
import datetime

class Priorities(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    priority = Column(Integer, unique=True, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    subscriptions = relationship('Subscriptions', backref="priority", uselist=True, lazy="dynamic")