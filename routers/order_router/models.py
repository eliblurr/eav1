from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Float, CheckConstraint
from sqlalchemy.orm import relationship, backref
from ..delivery_router.models import Delivery, DeliveryAddress, DeliveryOption, DeliveryTimeline
from ..payment_router.models import Payment
from database import Base, SessionLocal
import datetime, utils

code = lambda length:utils.gen_alphanumeric_code_lower(length)

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True, default=code(35), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_state_id = Column(Integer, ForeignKey("order_state.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    order_bill = relationship('OrderBill', backref='order', uselist=False, cascade='all,delete')
    order_delivery = relationship('Delivery', backref='order', uselist=False, cascade="all,delete")
    order_items = relationship('OrderItems', uselist=True, backref='order')
  
class OrderState(Base):
    __tablename__ = "order_state"
    __table_args__ = (
        # CheckConstraint('coalesce(timeline_id , title ) is not null;', name='only one default'),
    )
    # SELECT COUNT(default) FROM Products WHERE default=

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    default = Column(Boolean, default=False, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    orders = relationship('Orders', backref='order_state', uselist=True, lazy="dynamic") 

class OrderBill(Base):
    __tablename__ = "order_bill"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    payment = relationship('Payment', backref="order_bill", uselist=False, cascade="all, delete")
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # promo_voucher

class OrderItems(Base):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey('orders.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False) 
    sub_total = Column(Float, nullable=False) 
    purchase_type_id = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)
    product = relationship('Products')

@event.listens_for(OrderState.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([OrderState( title='processing', description="your order has been placed")])
    db.commit()

# "before_insert"
# "before_insert"