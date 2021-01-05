from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import asc
from typing import List
import sys, utils

logger = utils.get_logger()

async def create_about_us(payload: schemas.CreateAboutUs, db:Session):
    try:
        # for about_us in payload:
        about_us = models.AboutUs(**payload.dict())
        db.add(about_us) 
        db.commit()
        db.refresh(about_us)
        return about_us
    except IntegrityError:
        db.rollback()
        # log here
        raise HTTPException(status_code=422, detail="unique constraint on index failed")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def update_about_us(id: int, payload: schemas.UpdateAboutUs, db: Session):
    if not await read_about_us_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.AboutUs).filter(models.AboutUs.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_about_us_by_id(id, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="unique constraint on index failed")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def delete_about_us(ids: List[int], db: Session):
    try:
        for id in ids:
            about_us = await read_about_us_by_id(id, db)
            if about_us:
                db.delete(about_us)
        db.commit()
        return True
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException(status_code=500)

async def read_about_us(search:str, value:str, db: Session):
    base = db.query(models.AboutUs)
    if search and value:
        try:
            base = base.filter(models.AboutUs.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.AboutUs.index)).all()
    return base.order_by(asc(models.AboutUs.index)).all()

async def read_about_us_by_id(id: int, db: Session):
    return db.query(models.AboutUs).filter(models.AboutUs.id == id).first()
