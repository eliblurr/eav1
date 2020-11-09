from sqlalchemy import update, and_, exc, asc
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id

async def create_faqs(payload:  List[schemas.CreateFAQs], db:Session):
    try:
        for faq in payload:
            faq = models.FAQs(**faq.dict())
            db.add(faq) 
        db.commit()
        return payload

    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail="unique constraint failed on index column")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def update_faq(id: int, payload: schemas.UpdateFAQs, db: Session):
    if not await read_faq_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        db.query(models.FAQs).filter(models.FAQs.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return payload

    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail="unique constraint failed on index column")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        # log error

async def delete_faqs(ids: List[int], db: Session):
    try:
        for id in ids:
            faq = await read_faq_by_id(id, db)
            if faq:
                db.delete(faq)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def read_faqs(search:str, value:str, db: Session):
    base = db.query(models.FAQs)
    if search and value:
        try:
            base = base.filter(models.FAQs.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.FAQs.index)).all()
    return base.order_by(asc(models.FAQs.index)).all()

async def read_faq_by_id(id: int, db: Session):
    return db.query(models.FAQs).filter(models.FAQs.id == id).first()
