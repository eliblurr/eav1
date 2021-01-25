from ..payment_type_router.crud import read_payment_type_by_id
from ..users_router.crud import read_user_by_id
from exceptions import NotFoundError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_, exc
from . import models, schemas
import sys

async def create_payment(payload: schemas.CreatePayment, db: Session):
    try:  
        if await read_payment_type_by_id(payload.payment_type_id, db) is None:
            raise NotFoundError("payment type not found") 
        new_payment = models.Payment(**payload.dict(exclude={'card'}), card_number_brand=payload.card.number.brand, card_number_masked=payload.card.number.masked )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except NotFoundError:
        raise HTTPException(status_code=404,detail="{}".format(sys.exc_info()[1]))
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()[1]))

async def read_payment(skip: int, limit: int, search: str, value:str, start_amount:float, end_amount:float, user_id:int, db: Session):
    try:
        base = db.query(models.Payment)
        if user_id and await read_user_by_id(user_id, db) is not None:
            base = base.filter(models.Payment.owner_id==user_id)
        if start_amount and end_amount:
            try: 
                base = base.filter(and_(models.Payment.amount <= end_amount, models.Payment.amount >= start_amount))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_payment_by_id(id: int, db: Session):
    return db.query(models.Payment).filter(models.Payment.id==id).first()

async def update_payment(id: int, payload: schemas.UpdatePayment, db: Session):
    if not await read_payment_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Payment).filter(models.Payment.id==id).update(payload.dict(exclude_unset=True).items())
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