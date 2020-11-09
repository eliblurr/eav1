from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_, desc
# import sys

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

async def create_priority(payload: schemas.PriorityCreate, db: Session):
    try:
        new_priority = models.Priorities(**payload.dict())
        db.add(new_priority)
        db.commit()
        db.refresh(new_priority)
        return new_priority
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="priority value should be unique")
    except:
        db.rollback()

async def delete_priority(id: int, db: Session):
    try:
        priority = await read_priority_by_id(id, db)
        db.delete(priority)
        db.commit()
        return True
    except:
        db.rollback()

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
    try:
        priority = await read_priority_by_id(id, db)
        if not priority:
            raise HTTPException(status_code=404)
        data = db.query(models.Priorities).filter(models.Priorities.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return bool(data)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="priority value should be unique")

    except:
       db.rollback() 

