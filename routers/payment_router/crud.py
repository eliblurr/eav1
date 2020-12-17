from ..payment_type_router.crud import read_payment_type_by_id
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import sys

async def create_payment(payload: schemas.CreatePayment, db: Session):

    if payload.payment_type_id and not await read_payment_type_by_id(payload.payment_type_id, db):
        raise HTTPException(status_code=404, detail="selected payment type with id {} does not exist".format(payload.payment_type_id))
    
    try:  
        new_payment = models.Payment(**payload.dict())
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment) 
        return new_payment
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="user with email {} already exists".format(payload.email))
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def read_payment(skip: int, limit: int, search: str, value:str, db: Session):
    try:
        base = db.query(models.Payment)
        if search and value:
            try:
                base = base.filter(models.Payment.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def read_payment_by_id(id: int, db: Session):
    return db.query(models.Payment).filter(models.Payment.id == id).first()

async def delete_payment(id: int, db: Session):
    try:
        payment = await read_payment_by_id(id, db)
        if payment:
            db.delete(payment)
            db.commit()
        return True
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def update_payment(id: int, payload: schemas.UpdatePayment, db: Session):
    if not await read_payment_by_id(id, db):
        raise HTTPException(status_code=404, detail="payment not found")
    try:
        payment = db.query(models.Payment).filter(models.Payment.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        return await read_payment_by_id(id, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))