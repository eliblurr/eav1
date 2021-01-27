from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc, and_
from . import models, schemas
import utils
import sys
import os

PROMO_CODE_LENGTH = os.environ.get('PROMO_CODE_LENGTH') or 8

async def create_promo(payload: schemas.CreatePromoVoucher, db: Session):
    while True:
        code = utils.gen_alphanumeric_code(length=PROMO_CODE_LENGTH)
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
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_promo(start:float, end:float, skip:int, limit:int, search:str, value:str, db: Session):
    base = db.query(models.PromoVouchers)
    if (start and end) and (start < end):
        return base.filter(and_(models.PromoVouchers.discount >= start,models.PromoVouchers.discount <= end)).offset(skip).limit(limit).all() 
    if search and value:
        try:
            base = base.filter(models.PromoVouchers.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_promo_by_id(id: int, db: Session):
    return db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).first()

async def update_promo(id: int, payload: schemas.UpdatePromoVoucher, db: Session):
    promo = await read_promo_by_id(id, db)
    if not promo:
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_promo_by_id(id, db)
    except IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()))

async def delete_promo(id: int, db: Session):
    try:
        promo_voucher = await read_promo_by_id(id,db)
        if promo_voucher:
            db.delete(promo_voucher)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def assign_promo(id, owner_id, db: Session):
    if not await get_user_by_id(owner_id, db):
        raise HTTPException( status_code=404, detail="User Not Found")
    if not await crud.read_promo_by_id(id,db):
        raise HTTPException( status_code=404, detail="Promo Voucher Not Found")
    try:
        updated = db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).update({'user_id':owner_id})
        db.commit()
        if bool(updated):
            return await crud.read_promo_by_id(id,db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def unassign_promo(id, db: Session):
    if not await read_promo_by_id(id, db):
        raise HTTPException( status_code=404)
    try:
        updated = db.query(models.PromoVouchers).filter(models.PromoVouchers.id == id).update({'user_id':None})
        db.commit()
        if bool(updated):
            return await crud.read_promo_by_id(id,db)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)



