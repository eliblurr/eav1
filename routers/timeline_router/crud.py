from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

async def create_timeline(payload: schemas.CreateTimeline, db: Session):
    try:  
        new_timeline = models.Timeline(**payload.dict())
        db.add(new_timeline)
        db.commit()
        db.refresh(new_timeline) 
        return new_timeline
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_timeline(skip: int, limit: int, search: str, value:str, db: Session):
    try:
        base = db.query(models.Timeline)
        if search and value:
            try:
                base = base.filter(models.Timeline.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def read_timeline_by_id(id: int, db: Session):
    return db.query(models.Timeline).filter(models.Timeline.id == id).first()

async def delete_timeline(id: int, db: Session):
    try:
        timeline = await read_timeline_by_id(id, db)
        if timeline:
            db.delete(timeline)
        db.commit()
        return True
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def update_timeline(id: int, payload: schemas.UpdateTimeline, db: Session):
    if not await read_timeline_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Timeline).filter(models.Timeline.id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        if bool(updated):
            return await read_timeline_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))