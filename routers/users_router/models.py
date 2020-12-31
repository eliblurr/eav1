from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from passlib.hash import pbkdf2_sha256 as sha256
from ..promo_router.models import PromoVouchers
from ..favorites_router.models import Favorites
from ..product_router.models import Products
from ..payment_router.models import Payment
from ..reviews_router.models import Reviews
from ..boards_router.models import Boards
from database import Base, SessionLocal
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=True)
    auth_type_id = Column(Integer, ForeignKey("auth_type.id"), nullable=False)
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=False)
    user_info = relationship('UserInfo', backref="user", uselist=False, cascade="all, delete")
    promo_vouchers = relationship('PromoVouchers', backref="user", uselist=True, cascade="all, delete", lazy='dynamic')
    boards = relationship('Boards', backref="user", uselist=True, lazy="dynamic", cascade="all, delete")
    favorites = relationship('Products', secondary='favorites', backref=backref('liked_by', lazy='dynamic'), lazy='dynamic')
    products = relationship('Products', backref="owner", uselist=True, cascade="all, delete", lazy='dynamic')
    reviews = relationship('Reviews', backref="author", uselist=True, cascade="all, delete", lazy="dynamic")
    # reset_password_token = relationship('ResetPasswordToken', backref="user", uselist=False, cascade="all, delete")
    # payments = relationship('Payment', backref="customer", uselist=True, cascade="all, delete", lazy='dynamic')

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey("users.id") ,nullable=False, unique=True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    users = relationship('User', backref="user_type")
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

@event.listens_for(UserType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ UserType(title='vendor'), UserType(title='consumer'), UserType(title='Administrator') ]), UserType(title='System Manager')
    db.commit()