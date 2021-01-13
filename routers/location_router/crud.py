from ..currency_router.crud import read_currency_by_id
from fastapi import Depends, HTTPException
from sqlalchemy import exc, inspect
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
import pandas as pd
import numpy as np
import sys
import io

supported_ext = ["xls", "xlsx", "xlsm", "xlsb", "xltx", "xltm", "xls", "xlt", "xml", "xlam", "xla", "xlw", "xlr", "csv"]
header = ['CITY', 'COUNTRY', 'SUB_COUNTRY', 'GEO_ID']

# country
async def create_country(payload: schemas.CreateCountry, db: Session):
    if await read_currency_by_id(payload.currency_id, db):
        raise HTTPException(status_code=404, detail="currency not found")
    try:
        country = models.Country(**payload.dict()) 
        db.add(country)
        db.commit()
        db.refresh(country)
        return country
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail="Integrity constraint failed")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_country(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Country)
    if search and value:
        try:
            base = base.filter(models.Country.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_country_by_id(id: int, db: Session):
    return db.query(models.Country).filter(models.Country.id == id).first()

async def update_country(id: int, payload: schemas.UpdateCountry, db: Session):
    if await read_country_by_id(id, db) is None:
        raise HTTPException(status_code=404)
    if payload.currency_id and await read_currency_by_id(payload.currency_id, db):
        raise HTTPException(status_code=404, detail="currency not found")
    try:
        updated = db.query(models.Country).filter(models.Country.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_country_by_id(id, db)
    except:
        db.rollback()
        raise HTTPException(status_code = 500)

async def delete_country(ids: List[int], db: Session):
    try:
        for id in ids:
            country = await read_country_by_id(id, db)
            if country:
                db.delete(country)
        db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def read_country_children(id: int, skip:int, limit:int, search:str, value:str, db: Session):
    base = await read_country_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.sub_countries
    if search and value:
        try:
            base = base.filter(models.SubCountry.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

# sub country
async def create_sub_country(payload: schemas.CreateSubCountry, db: Session):
    if await read_country_by_id(payload.country_id, db) is None:
        raise HTTPException(status_code=404, detail="Country not found") 
    try:
        sub_country = models.SubCountry(**payload.dict()) 
        db.add(sub_country)
        db.commit()
        db.refresh(sub_country)
        return sub_country
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=422, detail="Integrity constraint failed")
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_sub_country(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.SubCountry)
    if search and value:
        try:
            base = base.filter(models.SubCountry.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_sub_country_by_id(id: int, db: Session):
    return db.query(models.SubCountry).filter(models.SubCountry.id == id).first()

async def update_sub_country(id: int, payload: schemas.UpdateSubCountry, db: Session):
    if await read_sub_country_by_id(id, db) is None:
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.SubCountry).filter(models.SubCountry.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_sub_country_by_id(id, db)
    except:
        db.rollback()
        raise HTTPException(status_code = 500)

async def delete_sub_country(ids: List[int], db: Session):
    try:
        for id in ids:
            sub_country = await read_sub_country_by_id(id, db)
            if sub_country:
                db.delete(sub_country)
        db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def read_sub_country_children(id: int, skip:int, limit:int, search:str, value:str, db: Session):
    base = await read_sub_country_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.locations
    if search and value:
        try:
            base = base.filter(models.Location.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

# location
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

async def create_location(payload: schemas.CreateLocation, db: Session):
    if await read_sub_country_by_id(payload.sub_country_id, db) is None:
        raise HTTPException(status_code=404, detail="Sub country not found")
    try:
        location = models.Location(**payload.dict()) 
        db.add(location)
        db.commit()
        db.refresh(location)
        return location
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()))
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_location(id: int, payload: schemas.UpdateLocation, db: Session):
    if await read_location_by_id(id, db) is None:
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Location).filter(models.Location.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_location_by_id(id, db)
    except:
        db.rollback()
        raise HTTPException(status_code = 500)

async def delete_location(ids: List[int], db: Session):
    try:
        for id in ids:
            location = await read_location_by_id(id, db)
            if location:
                db.delete(location)
        db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500)

# fileio
async def create_location_from_file(file, db: Session):
    if len(file.filename.split('.')) != 2:
        raise HTTPException(status_code=400, detail="try_name.ext")   
    
    name, ext = file.filename.split('.')
    if not ext in supported_ext:
        raise HTTPException(status_code=400, detail="file format not supported")
    
    file = await file.read()
    
    if ext == "csv":
        try:
            df = pd.read_csv(io.BytesIO(file), delimiter=',', names=header)
        except ValueError:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500)
    else: 
        try:
            df = pd.read_excel(file, names=header)
        except ValueError:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500)

    locations = np.array(df[header].replace(np.nan, None).drop_duplicates())
    i = 0
    try:
        for item in locations:
            sub_country = db.query(models.SubCountry).filter(models.SubCountry.name == item[2]).first()
            if sub_country is None:
                country = db.query(models.Country).filter(models.Country.name == item[1]).first()
                if country is None:
                    country = models.Country(name=item[1])
                    db.add(country)
                    db.flush()
                sub_country = models.SubCountry(name=item[2], country_id=country.id)
                db.add(sub_country)
                db.flush()
            try:
                loc = models.Location(name=item[0], geo_name_id=item[3], sub_country_id=sub_country.id) 
                db.add(loc)
                db.flush()
            except exc.IntegrityError:
                db.rollback()
                continue
        db.commit()
        return True
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
 