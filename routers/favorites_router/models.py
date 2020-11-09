from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from database import Base

from ..product_router.models import Products

class Favorites(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    product_id = Column(Integer, ForeignKey('products.id'),primary_key = True)
