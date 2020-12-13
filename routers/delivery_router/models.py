from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Delivery(Base):
     __tablename__ = "delivery"

     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     title = Column(String, nullable=False)
     metatitle = Column(String, nullable=True)
     description = Column(String, nullable=True)
     duration = Column(Integer,  nullable=False)
     price = Column(Float, nullable=False)
     status = Column(Boolean)

     created_date = Column(DateTime, default=datetime.datetime.utcnow)
     updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
