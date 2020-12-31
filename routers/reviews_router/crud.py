from ..product_router.crud import read_product_by_id
from ..auth_router.crud import read_user_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc, and_
from . import models, schemas
from typing import List
import sys

async def create_review(payload: schemas.CreateReview, product_id: int, user_id: int, db: Session):
    product = await read_product_by_id(product_id, db)
    res = (product is not None, await read_user_by_id(user_id, db) is not None)
    if all(res):
        pass
    else:
        raise HTTPException(status_code=404, detail="{} not found".format('product' if not(res[0]) else 'user' ))
    res = (await read_user_product_review(product_id, user_id, db) is None, product.owner_id != user_id)
    if all(res):
        pass
    else:
        raise HTTPException(status_code=400, detail="{}".format("user has already reviewed this product" if not(res[0]) else "product owner cannot review own product"))
    try:
        review = models.Reviews(**payload.dict(), product_id = product_id, user_id = user_id)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_review_by_id(id: int, db: Session):
    return db.query(models.Reviews).filter(models.Reviews.id == id).first()

async def update_review(id: int, author_id:int, payload:schemas.UpdateReview, db: Session):
    review = await read_review_by_id(id, db)
    if not review:
        raise HTTPException(status_code=404)
    if not await read_user_product_review(review.product_id, author_id, db):
        raise HTTPException(status_code=400)
    try:
        updated = db.query(models.Reviews).filter(models.Reviews.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_review_by_id(id, db)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_review(id: int, author_id:int,db: Session):
    try:
        review = await read_review_by_id(id, db)
        if review and await read_user_product_review(review.product_id, author_id, db):
            db.delete(review)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_user_product_review(product_id: int, user_id: int, db: Session):
    return db.query(models.Reviews).filter(and_(models.Reviews.user_id == user_id,models.Reviews.product_id == product_id)).first() 