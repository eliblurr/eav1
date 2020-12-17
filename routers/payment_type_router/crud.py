from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import sys

async def create_payment_type(payload: schemas.CreatePaymentType, db: Session):
    try:  
        new_payment_type = models.PaymentType(**payload.dict())
        db.add(new_payment_type)
        db.commit()
        db.refresh(new_payment_type) 
        return new_payment_type
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="user with email {} already exists".format(payload.email))
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

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
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

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
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    
async def update_payment_type(id: int, payload: schemas.UpdatePaymentType, db: Session):
    if not await read_payment_type_by_id(id, db):
        raise HTTPException(status_code=404, detail="payment type not found")
    try:
        payment_type = db.query(models.PaymentType).filter(models.PaymentType.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        return await read_payment_type_by_id(id, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))