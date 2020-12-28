from sqlalchemy import Column, Integer, String, DateTime, event, Boolean
from main import SessionLocal
from database import Base
import datetime

class WeightUnit(Base):
    __tablename__ = "weight_unit"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=False, unique=True)
    symbol = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

@event.listens_for(WeightUnit.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ WeightUnit(title='kilogram', symbol='kg'), WeightUnit(title='pound', symbol='lb') ])
    db.commit()