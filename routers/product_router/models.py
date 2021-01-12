from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from ..purchase_type_router.models import PurchaseType
from ..weight_unit_router.models import WeightUnit
from ..currency_router.models import Currency
from ..reviews_router.models import Reviews
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=False)
    serial_number = Column(String, nullable=True)
    available_quantity = Column(Integer, nullable=False)
    initial_quantity = Column(Integer, nullable=False)
    status = Column(Boolean, nullable = False, default = True)
    weight = Column(Float, nullable=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    images = relationship('ProductImages', backref="product", uselist=True, cascade="all, delete")
    reviews = relationship('Reviews', backref="product", uselist=True, cascade="all, delete", lazy='dynamic')
    payment_info = relationship('ProductPaymentInfo', backref="product", uselist=True)
    weight_unit = relationship('WeightUnit', backref="products", uselist=False)
    weight_unit_id = Column(Integer, ForeignKey("weight_unit.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # backrefs
    # categories
    # board
    # events
    # liked_by
    # locations

class ProductImages(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    image_url = Column(String, nullable=False)
    folder_name = Column(String, nullable=False)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ProductPaymentInfo(Base):
    __tablename__ = "product_payment_info"
    __table_args__ = (
        UniqueConstraint('product_id', 'purchase_type_id', name='_product_purchase_'),
    )

    duration = Column(Integer, nullable=True)
    batch_price = Column(Float, nullable=False)
    batch_size = Column(Integer, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    currency = relationship('Currency')
    purchase_type = relationship('PurchaseType')
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    currency_id = Column(Integer,ForeignKey("currency.id"), primary_key=True)
    purchase_type_id = Column(Integer, ForeignKey("purchase_type.id"), nullable=False, primary_key=True)
    
    # currency_id = Column(Integer,ForeignKey("currency.id"), nullable=False) 
    # timeline_id = Column(Integer, ForeignKey("timeline.id"), primary_key=True)
    # pass
    # __tablename__ = "delivery_timeline"
    #  __table_args__ = (
    #       UniqueConstraint('delivery_id', 'timeline_id', 'title', 'index', name='_delivery_timeline_dtti'),
    #       UniqueConstraint('delivery_id', 'timeline_id', 'title', name='_delivery_timeline_dtt'),
    #       UniqueConstraint('delivery_id', 'timeline_id', 'index', name='_delivery_timeline_dti'),
    #       UniqueConstraint('delivery_id', 'index', name='_delivery_timeline_di'),
    #       UniqueConstraint('delivery_id', 'title', name='_delivery_timeline_dt'),
    #  )
    #  delivery_id = Column(Integer, ForeignKey("delivery.id"), primary_key=True)
    #  timeline_id = Column(Integer, ForeignKey("timeline.id"), primary_key=True)
    #  index = Column(Integer, nullable=False,  primary_key=True)
    #  title = Column(String, nullable=True)
    #  metatitle = Column(String, nullable=True)
    #  description = Column(String, nullable=True)
    #  status = Column(Boolean, default=True, nullable=True)
    #  date_created = Column(DateTime, default=datetime.datetime.utcnow)
    #  date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    #  timeline = relationship("Timeline", back_populates="delivery")
    #  delivery = relationship("Delivery", back_populates="timeline")