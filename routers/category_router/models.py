from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship, backref
from ..product_router.models import Products
from database import Base
import datetime

class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    images = relationship('CategoryImages', backref="category", uselist=True, cascade="all, delete")
    category_items = relationship('Products', secondary='category_items', backref=backref('categories', lazy='dynamic'), lazy='dynamic')

class CategoryItems(Base):
    __tablename__ = 'category_items'

    category_id = Column(Integer, ForeignKey('categories.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)

class CategoryImages(Base):
    __tablename__ = "category_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    image_url = Column(String, nullable=True)
    folder_name = Column(String, nullable=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

