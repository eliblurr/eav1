from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from ..product_router.models import Products
from ..product_router.models import Products
from database import Base, SessionLocal
import datetime
import csv

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    sub_country = Column(String, nullable=True)
    geo_name_id = Column(Integer, nullable=True)
    status = Column(Boolean, nullable = False, default = True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    location_items = relationship('Products', secondary='location_items', backref=backref('locations', lazy='dynamic'), lazy='dynamic')

class LocationItems(Base):
    __tablename__ = "location_items"

    location_id = Column(Integer, ForeignKey('locations.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)

@event.listens_for(Location.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    with open("routers/location_router/location_data.csv") as location_data:
        reader = csv.reader(location_data)
        for row in reader:
            location = Location(name = row[0],country = row[1],sub_country = row[2],geo_name_id = row[3])
            db.add(location)
            # data.append(row)
    # for row in data:
    #     location = Location(name = row[0],country = row[1],sub_country = row[2],geo_name_id = row[3])
    #     db.add(location)
    db.commit()