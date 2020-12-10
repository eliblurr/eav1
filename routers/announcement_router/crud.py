from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..product_router.crud import read_products_by_id
from  sqlalchemy.sql.expression import func
from sqlalchemy import update, and_
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from typing import List
from main import get_db
import utils
import sys

async def create_announcement(payload:  schemas.CreateAnnouncement, db:Session):
    try:
        announcement = models.Announcement(**payload.dict())
        db.add(announcement) 
        db.commit()
        db.refresh(announcement)
        return announcement
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="Operation failed")

async def update_announcement(id: int, payload: schemas.UpdateAnnouncement, db: Session):
    if not await read_announcement_by_id(id, db):
        raise HTTPException( status_code=404)
    try: 
        db.query(models.Announcement).filter(models.Announcement.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_announcement_by_id(id, db)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="Operation failed")

async def delete_announcement(id: int, db: Session):
    try:
        announcement = await read_announcement_by_id(id, db)
        if announcement:
            db.delete(announcement)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="Operation failed")

async def read_announcement(search:str, value:str, db: Session):
    base = db.query(models.Announcement)
    if search and value:
        try:
            base = base.filter(models.Announcement.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.all()
    return base.all()

async def read_announcement_by_id(id: int, db: Session):
    return db.query(models.Announcement).filter(models.Announcement.id == id).first()

async def read_random_announcement(db: Session):
    return db.query(models.Announcement).filter(models.Announcement.is_active == True).order_by(func.random()).first()
