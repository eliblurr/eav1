from sqlalchemy import Column, ForeignKey, DateTime, Integer
from ..product_router.models import Products
from database import Base
import datetime

class Favorites(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)
