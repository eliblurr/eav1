from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, backref
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from . import models

import secrets

from ..promo_router.models import PromoVouchers
from ..boards_router.models import Boards
from ..favorites_router.models import Favorites

from ..product_router.models import Products

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    auth_type_id = Column(Integer, ForeignKey("auth_type.id"), nullable=True )
    
    user_info = relationship('UserInfo', backref="user", uselist=False, cascade="all, delete")
    promo_vouchers = relationship('PromoVouchers', backref="user", uselist=True, cascade="all, delete", lazy='dynamic')
    boards = relationship('Boards', backref="user", uselist=True,lazy="dynamic", cascade="all, delete")
    favorites = relationship('Products', secondary='favorites', backref=backref('user', lazy='dynamic'), lazy='dynamic')
    reset_password_token = relationship('ResetPasswordToken', backref="user", uselist=False, cascade="all, delete")
    products = relationship('Products', backref="owner", uselist=True, cascade="all, delete", lazy='dynamic')


    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id") ,nullable=False, unique=True)

    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_verified = Column(Boolean,nullable=False)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ResetPasswordToken(Base):
    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id") , unique=True)
    token = Column(String, index=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def generate_token():
        token = secrets.token_urlsafe(4)
        return sha256.hash(token)

    @staticmethod
    def verify_token(token, hash):
        return sha256.verify(token, hash)
# authentication Type
class AuthType(Base):
    __tablename__ = "auth_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    users = relationship('User', backref="auth_type")

@event.listens_for(AuthType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([
        AuthType(title='local'),
        AuthType(title='non_local')
    ])
    db.commit()
