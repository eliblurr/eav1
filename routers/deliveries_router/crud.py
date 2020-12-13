from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import update, and_, asc
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import utils
import sys

async def add_delivery(payload: schemas.DeliveryCreate, db: Session):
    try:
        delivery = models.Delivery(**payload.dict())
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{} : {}".format(sys.exc_info()[0], sys.exc_info()[1] ) )

async def read_delivery(skip, limit, search, value, db: Session):
    base = db.query(models.Delivery)
    if search and value:
        try:
            base = base.filter(models.Delivery.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_delivery_by_id(id: int, db: Session):
    return db.query(models.Delivery).filter(models.Delivery.id == id).first()

async def delete_delivery(id: int, db: Session):
    try:
        delivery = await read_delivery_by_id(id, db)
        if delivery:
            db.delete(delivery)
            db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def update_delivery(id: int, payload: schemas.DeliveryUpdate, db: Session):
    try:
        res = db.query(models.Delivery).filter(models.Delivery.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        return await read_delivery_by_id(id, db)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )