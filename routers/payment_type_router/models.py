from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, Float,  DateTime, Float
from ..payment_router.models import Payment
from database import Base, SessionLocal
from sqlalchemy.orm import relationship
import datetime

class PaymentType(Base):
    __tablename__ = 'payment_type'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    payments = relationship('Payment', backref="payment_type", uselist=True)

@event.listens_for(PaymentType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ PaymentType(title='Visa'), PaymentType(title='MasterCard'), PaymentType(title='Paypal') ])
    db.commit()

