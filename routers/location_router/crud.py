from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_
from typing import List

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


async def read_location(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Location)
    if search and value:
        try:
            base = base.filter(models.Location.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_location_by_id(id: int, db: Session):
    return db.query(models.Location).filter(models.Location.id == id).first()

async def create_location(location: schemas.CreateLocation, db: Session):
    try:
        location = models.Location(**location.dict()) 
        db.add(location)
        db.commit()
        db.refresh(location)
        return location
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def create_location_from_file(location: List[schemas.CreateLocation], db: Session):
    for item in location:
        loc = models.Location(**item) 
        db.add(loc)
    db.commit()
    return location

async def update_location(id: int, payload: schemas.UpdateLocation, db: Session):
    if await read_location_by_id(id, db) is None:
        raise HTTPException(status_code=404)
    try:
        db.query(models.Location).filter(models.Location.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_location_by_id(id, db)

    except:
        db.rollback()
        raise HTTPException(status_code = 500)

async def delete_location(id: int, db: Session):
    # for id in ids:
    try:
        location = await read_location_by_id(id, db)
        if location:
            db.delete(location)
        db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500)
