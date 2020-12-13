from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship, backref
from database import Base, metadata, engine
import datetime

class Announcement(Base):
    __tablename__ = "announcement"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

    # priority
