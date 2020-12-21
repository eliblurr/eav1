from sqlalchemy import Column, Integer, String, event, DateTime
from main import SessionLocal
from database import Base
import datetime

class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=False, unique=True)
    symbol = Column(String, nullable=True, unique=True)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

@event.listens_for(Currency.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ Currency(title='USD', symbol='$'), Currency(title='GBP', symbol='£') ])
    db.commit()