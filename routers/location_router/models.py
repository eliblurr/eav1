from sqlalchemy import event,Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship, backref

import datetime

from database import Base, metadata, engine, SessionLocal

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    sub_country = Column(String, nullable=True)
    geo_name_id = Column(Integer, nullable=True)


import csv

@event.listens_for(Location.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    # read from file and put in db
    data=[]
    with open("routers/location_router/location_data.csv") as location_data:
        reader = csv.reader(location_data)
        for row in reader:
            data.append(row)
    

    for row in data:
        location = Location(name = row[0],country = row[1],sub_country = row[2],geo_name_id = row[3])
        db.add(location)

    db.commit()

    