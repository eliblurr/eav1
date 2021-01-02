from ..payment_type_router.crud import read_payment_type_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import and_
from sqlalchemy import exc
import sys

# create
# read and filter
# read by id
# update
# delete

async def create_payment(payload: schemas.CreatePayment, db: Session):
    if await read_payment_type_by_id(payload.payment_type_id, db) is None:
        raise HTTPException(status_code=404)  
    try:  
        pass
        # new_payment = models.Payment(**payload.dict())
        # db.add(new_payment)
        # db.commit()
        # db.refresh(new_payment) 
        # return new_payment
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_payment(skip: int, limit: int, search: str, value:str, start_amount:float, end_amount:float, db: Session):
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
    return db.query(models.Payment).filter(models.Payment.id==id).first()

async def filter_payment(skip: int, limit: int, lower_boundary: float, upper_boundary:float, db: Session):
    try:
        base = db.query(models.Payment)
        if lower_boundary and upper_boundary:
            try: 
                base = base.filter(and_(
                    models.Payment.amount <= upper_boundary,
                    models.Payment.amount >= lower_boundary
                ))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def delete_payment(id: int, db: Session):
    try:
        payment = await read_payment_by_id(id, db)
        if payment:
            db.delete(payment)
            db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_payment(id: int, payload: schemas.UpdatePayment, db: Session):
    if not await read_payment_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Payment).filter(models.Payment.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        if updated:
            return await read_payment_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)