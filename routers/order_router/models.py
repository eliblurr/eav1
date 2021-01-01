from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from ..delivery_router.models import Delivery
from ..payment_router.models import Payment
from database import Base, SessionLocal
import datetime

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_state_id = Column(Integer, ForeignKey("order_state.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    order_bill = relationship('OrderBill', backref='order', uselist=False, cascade='all,delete')
    order_delivery = relationship('Delivery', backref='order', uselist=False, cascade="all,delete")
    order_items = relationship('Products', secondary='order_items', backref=backref('order', lazy='dynamic'), lazy='dynamic')
  
class OrderState(Base):
    __tablename__ = "order_state"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    status = Column(Boolean, default=True, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    orders = relationship('Orders', backref='order_state', uselist=True, lazy="dynamic")

class OrderBill(Base):
    __tablename__ = "order_bill"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Boolean, default=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    payment = relationship('Payment', backref="bill", uselist=False, cascade="all, delete", lazy='dynamic')
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class OrderItems(Base):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey('orders.id'),primary_key = True)
    item_id = Column(Integer, ForeignKey('products.id'),primary_key = True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)    
    duration = Column(Integer, nullable=True)
    # purchase type
    # duration

# # rental
# # purchase
# order
# order_bill
# order_items
# order_delivery
# order_delivery_timeline
# order_payment


# order_timeline = relationship('OrderTimeline', backref="order", uselist=True, cascade="all, delete",lazy='dynamic')

# order owner

# class OrderTimeline(Base):
#     __tablename__ = "order_timeline"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     metatitle = Column(String, nullable=True)
#     description = Column(String, nullable=True)
#     start_date = Column(DateTime, default=datetime.datetime.utcnow)
#     end_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
#     status = Column(Boolean, default=True)

#     created_date = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

#     order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
#     timeline_id = Column(Integer, ForeignKey("timeline.id"), nullable=True)


    
