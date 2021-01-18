from sqlalchemy import event, Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
# from ..delivery_router.models import DeliveryTimeline
from database import Base, SessionLocal
import datetime

class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # delivery = relationship('DeliveryTimeline', back_populates="timeline")

@event.listens_for(Timeline.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([Timeline( title='custom', description="create timeline specific to delivery"), Timeline( title='delivery under review', description="this may take some time")])
    db.commit()
