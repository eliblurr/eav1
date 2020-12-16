from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from ..reviews_router.models import Reviews
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(Integer, nullable = False)  
    rental = Column(Boolean, nullable = False, default = True)
    purchase = Column(Boolean, nullable = False, default = True)
    reviews = relationship('Reviews', backref="product", uselist=True, cascade="all, delete",lazy='dynamic')

    status = Column(Boolean, nullable = False, default = True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # category_items = relationship('Products', secondary='category_items', backref=backref('category', lazy='dynamic'), lazy='dynamic')


    # board = relationship('Boards', secondary='board_items', lazy='dynamic', cascade="all, delete")
    
# class PurchaseType(Base):
#     __tablename__ = "purchase_type"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     metatitle = Column(String, nullable=True)
#     description = Column(String, nullable=True)
#     status = Column(Boolean)

#     created_date = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_date = Column(DateTime, default=datetime.datetime.utcnow)

# @event.listens_for(PurchaseType.__table__, 'after_create')
# def insert_initial_values(*args, **kwargs):
#     db = SessionLocal()
#     db.add_all([PurchaseType(title='rental', status=True), PurchaseType(title='purchase', status=True)])
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