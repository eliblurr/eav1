from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import asc, exc
from . import models, schemas
from typing import List
import sys

async def create_tC_blocks(payload: schemas.CreateTC, db: Session):
    try:
        tC_block = models.TC(**payload.dict())
        db.add(tC_block) 
        db.commit()
        db.refresh(tC_block)
        return tC_block
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_tC_blocks(id: int, payload: schemas.UpdateTC, db: Session):
    if not await read_tC_block_by_id(id, db):
        raise HTTPException(status_code=404)
    try:  
        updated = db.query(models.TC).filter(models.TC.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_tC_block_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

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
        raise HTTPException(status_code=500)

async def read_tC_blocks(skip:int, limit:int, search:str, value:str, db: Session):
    base = db.query(models.TC)
    if search and value:
        try:
            base = base.filter(models.TC.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.TC.index)).offset(skip).limit(limit).all()
    return base.order_by(asc(models.TC.index)).offset(skip).limit(limit).all()

async def read_tC_block_by_id(id: int, db: Session):
    return db.query(models.TC).filter(models.TC.id == id).first()
    
