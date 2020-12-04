from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, backref
from database import Base, SessionLocal
from ..users_router.models import User
import datetime, utils

class ResetPasswordCodes(Base):
    __tablename__ = 'reset_password_codes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    code = Column(String, unique=True)
    status = Column(Boolean)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def generate_code():
        return utils.gen_alphanumeric_code(9)

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow)

class AuthType(Base):
    __tablename__ = "auth_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)

    users = relationship('User', backref="auth_type")

@event.listens_for(AuthType.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db = SessionLocal()
    db.add_all([ AuthType(title='local'), AuthType(title='non_local') ])
    db.commit()