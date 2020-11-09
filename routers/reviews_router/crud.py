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
from ..product_router.models import Products
from ..auth_router.crud import get_user_by_id

async def create_review(payload: schemas.ReviewsCreate, product_id: int, user_id: int, db: Session):
    product = await read_products_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404)

    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404)

    
    if await read_user_product_review(product_id, user_id, db):
        raise HTTPException(400, detail="you have already reviewed this product")
    
    
    try:
        review = models.Reviews(**payload.dict(), product = product, author = user.user_info)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def read_review_by_id(id: int, db: Session):
    return db.query(models.Reviews).filter(models.Reviews.id == id).first()

async def delete_review(id: int, db: Session):
    
    try:
        review =  await read_review_by_id(id, db)
        if review:
            db.delete(review)
        db.commit()
        return True
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def delete_user_product_review(product_id: int, user_id: int, db: Session):

    try:
        review = await read_user_product_review(product_id, user_id, db)
        
        if review:
            db.delete(review)
            
        db.commit()
        return True
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def update_review(id: int, payload:schemas.ReviewsUpdate, db: Session):
 
    review =  await read_review_by_id(id, db)
    if not review:
        raise HTTPException(status_code=404)
    
    try:
        review = db.query(models.Reviews).filter(models.Reviews.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_review_by_id(id, db)
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)

    
async def read_product_reviews(id: int, skip: int, limit: int, db: Session):
    if not await read_products_by_id(id, db):
        raise HTTPException(status_code=404)
    return db.query(Products).filter(Products.id == id).first().reviews.offset(skip).limit(limit).all()


async def read_user_product_review(product_id: int, user_id: int, db: Session):
    return db.query(models.Reviews).filter(and_(models.Reviews.user_id == user_id,models.Reviews.product_id == product_id)).first()