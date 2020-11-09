from sqlalchemy import update, and_, exc, asc
from sqlalchemy.orm import Session
from fastapi import HTTPException


from typing import List

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id

async def create_tC_blocks(payload:  List[schemas.CreateTC], db: Session):
    try:
        for tC_block in payload:
            tC_block = models.TC(**tC_block.dict())
            db.add(tC_block) 
        db.commit()
        # db.refresh(tC_block)
        return payload

    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def update_tC_blocks(id: int, payload: schemas.UpdateTC, db: Session):
    if not await read_tC_block_by_id(id, db):
        raise HTTPException(status_code=404)
    try:        
        block = db.query(models.TC).filter(models.TC.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_tC_block_by_id(id, db)

    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")

    except:
        db.rollback()

async def delete_tC_block(ids: List[int], db: Session):
    try:
        for id in ids:
            tC_block = await read_tC_block_by_id(id, db)
            if tC_block:
                db.delete(tC_block)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def read_tC_blocks(search:str, value:str, db: Session):
    base = db.query(models.TC)
    if search and value:
        try:
            base = base.filter(models.TC.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.TC.index)).all()
    return base.order_by(asc(models.TC.index)).all()

async def read_tC_block_by_id(id: int, db: Session):
    return db.query(models.TC).filter(models.TC.id == id).first()
    
