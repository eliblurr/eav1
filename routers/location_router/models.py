from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
# from ..delivery_router.models import DeliveryOption
from ..weight_unit_router.models import WeightUnit
from ..currency_router.models import Currency
from ..product_router.models import Products
from database import Base, SessionLocal
from ..ad_router.models import Ads
import datetime

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    sub_countries = relationship('SubCountry', backref="country", uselist=True, cascade="all, delete", lazy='dynamic')
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    currency = relationship('Currency', backref="locations")
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    weight_unit = relationship('WeightUnit', backref="locations")
    weight_unit_id = Column(Integer, ForeignKey("weight_unit.id"), nullable=False)

class SubCountry(Base):
    __tablename__ = "sub_countries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    zip_code = Column(String, nullable=True, unique=False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    locations = relationship('Location', backref="sub_country", uselist=True, cascade="all, delete", lazy='dynamic')
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    geo_name_id = Column(Integer, nullable=False, unique=True)
    zip_code = Column(String, nullable=True, unique=False)
    status = Column(Boolean, nullable = False, default = True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    sub_country_id = Column(Integer, ForeignKey('sub_countries.id'))
    location_items = relationship('Products', secondary='location_items', backref=backref('locations', lazy='dynamic'), lazy='dynamic')
    location_ads = relationship('Ads', secondary='location_ads', backref=backref('locations', lazy='dynamic'), lazy='dynamic')
    loction_delivery_options = relationship('DeliveryOption', secondary='loction_delivery_options', backref=backref('locations', lazy='dynamic'), lazy='dynamic')

class LocationItems(Base):
    __tablename__ = "location_items"

    location_id = Column(Integer, ForeignKey('locations.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)

class LocationAds(Base):
    __tablename__ = "location_ads"

    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    ad_id = Column(Integer, ForeignKey('ads.id'), primary_key=True)

class LocationDeliveryOptions(Base):
    __tablename__ = "loction_delivery_options"

    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    delivery_option_id = Column(Integer, ForeignKey('delivery_options.id'), primary_key=True)