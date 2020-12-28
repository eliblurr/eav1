from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import asc
from typing import List
import sys

async def create_policies(payload: schemas.CreatePolicies, db:Session):
    try:
        policy = models.Policies(**payload.dict())
        db.add(policy) 
        db.commit()
        db.refresh(policy)
        return policy
    except IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_policy(id: int, payload: schemas.UpdatePolicies, db: Session):
    if not await read_policy_by_id(id, db):
        raise HTTPException(status_code = 404)
    try:
        updated = db.query(models.Policies).filter(models.Policies.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_policy_by_id(id, db)
    except IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_policy(ids: List[int], db: Session):
    try:
        for id in ids:
            policy = await read_policy_by_id(id, db)
            if policy:
                db.delete(policy)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_policies(skip:int, limit:int,search:str, value:str, db: Session):
    base = db.query(models.Policies)
    if search and value:
        try:
            base = base.filter(models.Policies.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.Policies.index)).offset(skip).limit(limit).all()
    return base.order_by(asc(models.Policies.index)).offset(skip).limit(limit).all()

async def read_policy_by_id(id: int, db: Session):
    return db.query(models.Policies).filter(models.Policies.id == id).first()
