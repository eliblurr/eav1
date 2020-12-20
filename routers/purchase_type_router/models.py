from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship, backref
from database import Base, SessionLocal
import datetime

from ..product_router.models import Products

class PurchaseType(Base):
    __tablename__ = "purchase_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    items = relationship('Products', backref="purchase_type", uselist=True, cascade="all, delete")

@event.listens_for(PurchaseType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ PurchaseType(title='rental'), PurchaseType(title='purchase'), PurchaseType(title='both') ])
    db.commit()
