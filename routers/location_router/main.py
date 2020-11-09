from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, schemas, models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys

from main import get_db, oauth2_scheme
import utils


router = APIRouter()

@router.post("/location/uploadfiles/", response_model= List[schemas.CreateLocation])
async def create_location_from_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    payload = []
    contents = await file.read()
    for row in contents.decode("utf-8").splitlines():
        row = row.split(',')
        tmp={
            'name':row[0],
            'country':row[1],
            'sub_country':row[2],
            'geo_name_id':int(row[3])
        }
        payload.append(tmp)

    return await crud.create_location_from_file(payload, db)

@router.post("/", description="create new Location",response_model=schemas.Location)
async def create_location(payload: schemas.CreateLocation, db: Session= Depends(get_db)):
    return await crud.create_location(payload, db)

@router.delete("/", description="delete location by id")
async def delete_location(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_location(id, db):  
        raise HTTPException( status_code=500, detail="Operation failed")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="get/search location",response_model=List[schemas.Location])
async def read_location(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_location(skip, limit, search, value, db)

@router.get("/{id}", description="get location by id",response_model=schemas.Location)
async def read_location_by_id(id: int, db: Session = Depends(get_db)):
    location = await crud.read_location_by_id(id, db)
    if location is None:
        raise HTTPException(status_code=404)
    return location

@router.patch("/{id}", description="update location details",response_model=schemas.Location)
async def update_location(id: int, payload: schemas.UpdateLocation, db: Session = Depends(get_db)):
    return await crud.update_location(id, payload, db)