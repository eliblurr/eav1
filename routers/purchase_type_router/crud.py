from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import exc
import sys

async def create_purchase_type(payload: schemas.CreatePurchaseType, db: Session):
    try:  
        purchase_type = models.PurchaseType(**payload.dict())
        db.add(purchase_type)
        db.commit()
        db.refresh(purchase_type) 
        return purchase_type
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)  

async def read_purchase_type(skip: int, limit: int, search: str, value:str, db: Session):
    try:
        base = db.query(models.PurchaseType)
        if search and value:
            try:
                base = base.filter(models.PurchaseType.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_purchase_type_by_id(id: int, db: Session):
    return db.query(models.PurchaseType).filter(models.PurchaseType.id == id).first()

async def update_purchase_type(id, payload: schemas.UpdatePurchaseType, db: Session):
    if not await read_purchase_type_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.PurchaseType).filter(models.PurchaseType.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        if bool(updated):
            return await read_purchase_type_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_purchase_type(id, db: Session):
    try:
        purchase_type = await read_purchase_type_by_id(id, db)
        if purchase_type:
            db.delete(purchase_type)
        db.commit()
        return True
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))