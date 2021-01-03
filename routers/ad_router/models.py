from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
import datetime

class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    style_id = Column(Integer, ForeignKey('styles.id'), nullable=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    images = relationship('AdImages', backref="ad", uselist=True, cascade="all, delete", lazy="dynamic")
    
class AdImages(Base):
    __tablename__ = "ad_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('ads.id'))
    image_url = Column(String, nullable=True)
    folder_name = Column(String, nullable=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Styles(Base):
    __tablename__ = "styles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    background_color = Column(String, nullable=True)
    text_color = Column(String, nullable=True)
    fontWeight = Column(Integer, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    ads = relationship('Ads', backref="style", uselist=True, lazy="dynamic")
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)