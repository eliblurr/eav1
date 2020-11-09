from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_
from typing import List

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id
from ..auth_router.crud import get_user_by_id
from ..auth_router.models import User

# add item to favorites
# remove item from favorites
# get user favorites

async def add_to_user_favorites(product_id: int, user_id: int, db: Session):
    try:
        user = await get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail= "User Not Found")

        product = await read_products_by_id(product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail= "Product Not Found")
        
        user.favorites.append(product)
        db.commit()

        return bool(user and product)

    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="product already a user favorite")
    except:
        raise HTTPException(status_code=500, detail="something went wrong")

async def remove_from_user_favorites(product_id: int, user_id: int, db: Session):
    try:
        user = await get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail= "User Not Found")

        product = await read_products_by_id(product_id, db)
        if not product:
            raise HTTPException(status_code=404, detail= "Product Not Found")
        
        user.favorites.remove(product)
        db.commit()

        return bool(user and product)

    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="product already a user favorite")

    except:
        raise HTTPException(status_code=500, detail="something went wrong")


async def get_user_favorites(user_id:int, skip: int, limit: int, db: Session):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail= "User Not Found")

    return db.query(User).filter(User.id == user_id).first().favorites.offset(skip).limit(limit).all()

        

