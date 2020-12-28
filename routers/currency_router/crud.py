from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

async def create_currency(payload: schemas.CreateCurrency, db: Session):
    try:  
        new_currency = models.Currency(**payload.dict())
        db.add(new_currency) 
        db.commit()
        db.refresh(new_currency)
        return new_currency
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail="IntegrityError: UNIQUE constraint failed")
    except:
        db.rollback()
        print("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)
    
async def read_currency(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Currency)
    if search and value:
        try:
            base = base.filter(models.Currency.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_currency_by_id(id: int, db: Session):
    return db.query(models.Currency).filter(models.Currency.id == id).first()

async def delete_currency(id: int, db: Session):
    try:
        currency = await read_currency_by_id(id, db)
        if currency:
            db.delete(currency)
            db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_currency(id: int, payload: schemas.UpdateCurrency, db: Session):
    if not await read_currency_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Currency).filter(models.Currency.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_currency_by_id(id, db)
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=422, detail="IntegrityError: UNIQUE constraint failed") 
    except:
        db.rollback()
        raise HTTPException(status_code=500)
