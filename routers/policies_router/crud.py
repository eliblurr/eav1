from sqlalchemy import update, and_, exc, desc, asc
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException


from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id

async def create_policies(payload: List[schemas.CreatePolicies], db:Session):
    try:
        for policy in payload:
            policy = models.Policies(**policy.dict())
            db.add(policy) 
        db.commit()
        return payload

    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def update_policy(id: int, payload: schemas.UpdatePolicies, db: Session):
    if not await read_policy_by_id(id, db):
        raise HTTPException(status_code = 404)
    try:
        db.query(models.Policies).filter(models.Policies.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_policy_by_id(id, db)

    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail = "unique constraint failed on index")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

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

async def read_policies(search:str, value:str, db: Session):
    base = db.query(models.Policies)
    if search and value:
        try:
            base = base.filter(models.Policies.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.order_by(asc(models.Policies.index)).all()
    return base.order_by(asc(models.Policies.index)).all()

async def read_policy_by_id(id: int, db: Session):
    return db.query(models.Policies).filter(models.Policies.id == id).first()
