from sqlalchemy import event, Boolean, Column, Integer, String, DateTime
from database import Base, SessionLocal
import datetime

class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

@event.listens_for(Timeline.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ Timeline(title='delivery under review', description="this may take some time")])
    db.commit()

