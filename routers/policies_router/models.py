from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base
import datetime

class Policies(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    index = Column(Integer, autoincrement=True, nullable=False, unique=True, index=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)