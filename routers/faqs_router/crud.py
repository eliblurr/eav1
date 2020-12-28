from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import asc
from typing import List
import sys

async def create_faqs(payload:  schemas.CreateFAQs, db:Session):
    try:
        faq = models.FAQs(**payload.dict())
        db.add(faq) 
        db.commit()   
        db.refresh(faq)     
        return faq
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail="unique constraint failed on index column")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code = 500)

async def update_faq(id: int, payload: schemas.UpdateFAQs, db: Session):
    if not await read_faq_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.FAQs).filter(models.FAQs.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_faq_by_id(id, db)
    except IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code = 422, detail="unique constraint failed on index column")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code = 500)

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
        raise HTTPException(status_code = 500)

async def read_faqs(skip:int, limit:int, search:str, value:str, db: Session):
    base = db.query(models.FAQs)
    if search and value:
        try:
            base = base.filter(models.FAQs.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.FAQs.index)).offset(skip).limit(limit).all()
    return base.order_by(asc(models.FAQs.index)).offset(skip).limit(limit).all()

async def read_faq_by_id(id: int, db: Session):
    return db.query(models.FAQs).filter(models.FAQs.id == id).first()
