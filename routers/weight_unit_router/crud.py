from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import utils
import sys

async def create_weight_unit(payload: schemas.CreateWeightUnit, db: Session):

    try:  
        new_weight_unit = models.WeightUnit(**payload.dict())
        db.add(new_weight_unit) 
        db.commit()
        db.refresh(new_weight_unit)
        return new_weight_unit

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )
    
async def read_weight_unit(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.WeightUnit)
    if search and value:
        try:
            base = base.filter(models.WeightUnit.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_weight_unit_by_id(id: int, db: Session):
    return db.query(models.WeightUnit).filter(models.WeightUnit.id == id).first()

async def delete_weight_unit(id: int, db: Session):
    try:
        weight_unit = await read_weight_unit_by_id(id, db)
        if weight_unit:
            db.delete(weight_unit)
            db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_weight_unit(id: int, payload: schemas.UpdateWeightUnit, db: Session):
    if not await read_weight_unit_by_id(id, db):
        raise HTTPException(status_code=404, status_code="currency not found")

    try:
        db.query(models.WeightUnit).filter(models.WeightUnit.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_weight_unit_by_id(id, db)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
    except:
        db.rollback()
        raise HTTPException(status_code=500)
