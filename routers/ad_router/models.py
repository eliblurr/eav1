from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets

class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    # predefined components
    component_id = Column(Integer, ForeignKey('ad_component.id'))
    ad_style = Column(Integer, ForeignKey('ad_style.id'))

    priority = Column(Integer)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AdStyles(Base):
    __tablename__ = "ad_styles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    background_color = Column(String, default='#2d3436')
    text_color = Column(String, default='#ffffff')

class AdComponent(Base):
    __tablename__ = "ad_components"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, default='#2d3436')
    # text_color = Column(String, default='#ffffff')


@event.listens_for(AdComponent.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([
        AdComponent(title='type1'),
        AdComponent(title='type2'),
        AdComponent(title='type3'),
    ])
    db.commit()