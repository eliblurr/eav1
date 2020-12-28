from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base
import datetime

class Announcement(Base):
    __tablename__ = "announcement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)