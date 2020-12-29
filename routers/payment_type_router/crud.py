from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

# exc.OperationalError

async def create_payment_type(payload: schemas.CreatePaymentType, db: Session):
    try:  
        new_payment_type = models.PaymentType(**payload.dict())
        db.add(new_payment_type)
        db.commit()
        db.refresh(new_payment_type) 
        return new_payment_type
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_payment_type(skip: int, limit: int, search: str, value:str, db: Session):
    try:
        base = db.query(models.PaymentType)
        if search and value:
            try:
                base = base.filter(models.PaymentType.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_payment_type_by_id(id: int, db: Session):
    return db.query(models.PaymentType).filter(models.PaymentType.id == id).first()

async def delete_payment_type(id: int, db: Session):
    try:
        payment_type = await read_payment_type_by_id(id, db)
        if payment_type:
            db.delete(payment_type)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
    
async def update_payment_type(id: int, payload: schemas.UpdatePaymentType, db: Session):
    if not await read_payment_type_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        payment_type = db.query(models.PaymentType).filter(models.PaymentType.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        return await read_payment_type_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)