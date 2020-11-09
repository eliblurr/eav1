from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date, Float
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

from database import Base, SessionLocal

from ..subscriptions_router.models import Subscriptions

from . import models

import secrets

class Priorities(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, nullable=True)
    metatitle = Column(String, nullable=True)
    description = Column(String, nullable=True)

    priority = Column(Integer, unique=True, nullable=False)

    subscriptions = relationship('Subscriptions', backref="priority", uselist=True)

    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)





#     # product_id
#     # priority_id
    # priority_id = Column(Integer, ForeignKey('priorities.id'),primary_key = True)
    # product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)

#     # tbd
#     user_id = Column(Integer, ForeignKey('users.id'),primary_key = True)

#     expiry = Column(DateTime)

#     date_created = Column(DateTime,  default=datetime.datetime.utcnow)
#     date_modified = Column(DateTime,  default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# put relationship in product
# board_items = relationship('Products', secondary='board_items', backref=backref('board', lazy='dynamic'))


# Handling Expiry date
# create a view that shows all items where Expiry Date = [Today]

# use trigger / schedular
# use trigger to create/update a scheduled event when user buys a subscription/priority


# What you need in MSSQL is a maintenance plan, if you set up a maintenance plan which executes a TSQL task, which then get all expired cources without expirery date set for instance and update those with today and send a mail.