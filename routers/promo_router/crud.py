from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_
# import sys

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..auth_router.crud import get_user_by_id




async def create_promo(payload: schemas.CreatePromoVoucher, db: Session):

    while True:
        code = utils.gen_alphanumeric_code(length=8)
        base = db.query(models.PromoVouchers).filter(models.PromoVouchers.promo_code == code).first()
        if base is None:
            break

    if payload.discount <= 0:
        raise HTTPException(status_code=400, detail="discount must be greater than 0")

    try:        
        new_promo_voucher = models.PromoVouchers(**payload.dict(),promo_code=code)
        db.add(new_promo_voucher)
        db.commit()
        db.refresh(new_promo_voucher)
        return new_promo_voucher
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Operation failed")

async def delete_promo(id: int, db: Session):
    try:
        promo_voucher = await read_promo_by_id(id,db)
        if promo_voucher:
            db.delete(promo_voucher)
        db.commit()
        return True
    except:
        db.rollback()

async def read_promo_by_id(id: int, db: Session):
    return db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).first()

async def read_promo(db: Session,start: float = 0.0, end: float = 0.0, skip: int = 0, limit: int = 100, search:str=None, value:str=None ):
    base = db.query(models.PromoVouchers)

    if start is not None and end and start < end:
        return base.filter(and_(models.PromoVouchers.discount >= start,models.PromoVouchers.discount <= end)).offset(skip).limit(limit).all()
       
    if search and value:
        try:
            base = base.filter(models.PromoVouchers.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()

    return base.offset(skip).limit(limit).all()
   

async def read_promo_by_code(code: str, db: Session):
    return db.query(models.PromoVouchers).filter(models.PromoVouchers.promo_code == code).first()

async def read_promo_by_owner(id: int, db: Session):
    return db.query(models.PromoVouchers).filter(models.PromoVouchers.user_id == id).all()

async def read_promo_by_discount(start: float, end: float, skip: int, limit: int, db: Session = Depends(get_db)):
    return db.query(models.PromoVouchers).filter(and_(
        models.PromoVouchers.discount >= start,
        models.PromoVouchers.discount <= end,
    )).offset(skip).limit(limit).all()

async def update_promo_by_id(id, payload: schemas.UpdatePromoVoucher, db):
    promo = await read_promo_by_id(id, db)
    if not promo:
        raise HTTPException(status_code=404)
    
    try:
        return
    except:
        db.rollback()

async def assign_promo(id, owner_id, db: Session):
    if not await get_user_by_id(owner_id, db):
        raise HTTPException( status_code=404, detail="User Not Found")

    if not  await crud.read_promo_by_id(id,db):
        raise HTTPException( status_code=404, detail="Promo Voucher Not Found")

    try:
        db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).update({'user_id':owner_id})
        db.commit()
        return await crud.read_promo_by_id(id,db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail = "Error whilst adding resource {}".format(str(e)))
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail = "Error whilst adding resource {}".format(str(e)))
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def unassign_promo(id, db: Session):
    if not  await crud.read_promo_by_id(id,db):
        raise HTTPException( status_code=404, detail="Promo Voucher Not Found")

    try:
        db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).update({'user_id':None})
        db.commit()
        return await crud.read_promo_by_id(id,db)
    except:
        db.rollback()



