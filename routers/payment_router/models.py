from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment = Column(String, nullable=True)
    card_number_brand = Column(String, nullable=True)
    card_number_masked = Column(String, nullable=True)
    amount = Column(Float, default=0.0, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    payment_type_id = Column(Integer, ForeignKey('payment_type.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)