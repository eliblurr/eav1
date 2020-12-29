from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc, desc
from . import models, schemas
import sys

async def create_priority(payload: schemas.PriorityCreate, db: Session):
    try:
        new_priority = models.Priorities(**payload.dict())
        db.add(new_priority)
        db.commit()
        db.refresh(new_priority)
        return new_priority
    except exc.IntegrityError as e:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_priority(id: int, db: Session):
    try:
        priority = await read_priority_by_id(id, db)
        if priority:
            db.delete(priority)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_priority_by_id(id: int, db: Session):
    return db.query(models.Priorities).filter(models.Priorities.id == id).first()

async def read_priorities(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Priorities)
    if search and value:
        try:
            base = base.filter(models.Priorities.__table__.c[search].like("%"+ value +"%"))
        except KeyError:
            return base.order_by(desc(models.Priorities.priority)).offset(skip).limit(limit).all()
    return base.order_by(desc(models.Priorities.priority)).offset(skip).limit(limit).all()

async def update_priority(id: int, payload: schemas.PriorityUpdate, db: Session):
    priority = await read_priority_by_id(id, db)
    if not priority:
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Priorities).filter(models.Priorities.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_priority_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
       db.rollback() 
       print("{}".format(sys.exc_info()))
       raise HTTPException(status_code=500)

