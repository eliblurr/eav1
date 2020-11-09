from sqlalchemy import update, and_, asc
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id


async def create_about_us(payload: List[schemas.CreateAboutUs], db:Session):
    try:
        for about_us in payload:
            about_us = models.AboutUs(**about_us.dict())
            db.add(about_us) 
        db.commit()

        return payload

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="unique constraint on index failed")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def update_about_us(id: int, payload: schemas.UpdateAboutUs, db: Session):
    if not await read_about_us_by_id(id, db):
        raise HTTPException(status_code=404)
    try:

        db.query(models.AboutUs).filter(models.AboutUs.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_about_us_by_id(id, db)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="unique constraint on index failed")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

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
        print("{}".format(sys.exc_info()))

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
