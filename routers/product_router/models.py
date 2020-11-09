from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

import datetime

from database import Base

from ..reviews_router.models import Reviews

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(Integer, nullable = False)  

    status = Column(Boolean, nullable = False, default = True)
    
    rental = Column(Boolean, nullable = False, default = True)
    purchase = Column(Boolean, nullable = False, default = True)

    reviews = relationship('Reviews', backref="product", uselist=True, cascade="all, delete",lazy='dynamic')

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)


    # board = relationship('Boards', secondary='board_items', lazy='dynamic', cascade="all, delete")
    


# # trigger
# @event.listens_for(Products.__table__, 'after_create')
# def insert_initial_values(*args, **kwargs):
#     db = SessionLocal()
#     db.add_all([
#         OrderType(title='rental'),
#         OrderType(title='purchase')
#     ])
#     db.commit()


# id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     title = db.Column(db.String(50), nullable = False)  
#     metaTitle = db.Column(db.String(50), nullable = True)  
#     images = db.Column(db.String(50), nullable = True)  
#     product_id = db.Column(db.String(50), nullable = True)
#     price = db.Column(db.Float(50), nullable = False)  
#     discount = db.Column(db.Float(50), nullable = True)  
#     quantity = db.Column(db.Integer, nullable = False)  
#     verified_seller = db.Column(db.Boolean)
#     description = db.Column(db.String(250), nullable = False)  
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     categories = db.relationship('Categories', secondary=product_categories, lazy='subquery',backref=db.backref('products', lazy=True))
#     date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
#     date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
#     events = db.relationship('Events', secondary=product_events, lazy='subquery', backref=db.backref('products',lazy=True))
#     reviews = db.relationship('Reviews', backref='product', lazy=True)
#     order_item = db.relationship('OrderItems', backref='product', lazy=True)