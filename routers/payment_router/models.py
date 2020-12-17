from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, Float,  DateTime, Float
from database import Base, SessionLocal
from sqlalchemy.orm import relationship
import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Boolean, default=True, nullable=False)
    amount = Column(Float, default=0.0, nullable=False)
    comment = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    payment_type_id = Column(Integer, ForeignKey("payment_type.id"), nullable=True)