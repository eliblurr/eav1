from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from . import crud, schemas, models
from sqlalchemy.orm import Session
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", description="create new Location",response_model=schemas.Location, status_code=status.HTTP_201_CREATED)
async def create_location(payload: schemas.CreateLocation, db: Session= Depends(get_db)):
    return await crud.create_location(payload, db)

@router.post("/files", description="add location from file", status_code=status.HTTP_201_CREATED)
async def create_location_from_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await crud.create_location_from_file(file, db)

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

@router.delete("/", description="delete location by id", status_code = status.HTTP_202_ACCEPTED)
async def delete_location(id: List[int], db: Session = Depends(get_db)):
    return await crud.delete_location(id, db)

router2 = APIRouter()

@router2.post("/", description="create new country", response_model=schemas.Country, status_code=status.HTTP_201_CREATED)
async def create_country(payload: schemas.CreateCountry, db: Session=Depends(get_db)):
    return await crud.create_country(payload, db)

@router2.get("/", description="get countries", response_model=List[schemas.Country])
async def read_country(search:str=None, value:str=None, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return await crud.read_country(skip, limit, search, value, db)

@router2.get("/{id}", description="get country by id", response_model=schemas.Country)
async def read_country_by_id(id: int, db: Session=Depends(get_db)):
    country = await crud.read_country_by_id(id, db)
    if country is None:
        raise HTTPException(status_code=404)
    return country

@router2.get("/{id}/sub_countries", description="get country sub countries/regions", response_model=List[schemas.SubCountry])
async def read_country_children(id: int, search:str=None, value:str=None, skip:int=0, limit:int=100, db: Session=Depends(get_db)):
    return await crud.read_country_children(id, skip, limit, search, value, db)

@router2.patch("/{id}", description="update country", response_model=schemas.Country)
async def update_country(id: int, payload: schemas.UpdateCountry, db: Session=Depends(get_db)):
    return await crud.update_country(id, payload, db)

@router2.delete("/{id}", description="delete country", status_code = status.HTTP_202_ACCEPTED)
async def delete_country(ids: List[int], db: Session=Depends(get_db)):
    return await crud.delete_country(ids, db)

router3 = APIRouter()

@router3.post("/", description="create sub country", response_model=schemas.SubCountry, status_code=status.HTTP_201_CREATED)
async def create_sub_country(payload: schemas.CreateSubCountry, db: Session=Depends(get_db)):
    return await crud.create_sub_country(payload, db)

@router3.get("/", description="get sub countries", response_model=List[schemas.SubCountry])
async def read_sub_country(search:str=None, value:str=None, skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    return await crud.read_sub_country(skip, limit, search, value, db)

@router3.get("/{id}", description="get sub country by id", response_model=schemas.SubCountry)
async def read_sub_country_by_id(id: int, db: Session=Depends(get_db)):
    sub_country = await crud.read_sub_country_by_id(id, db)
    if sub_country is None:
        raise HTTPException(status_code=404)
    return sub_country

@router3.get("/{id}/locations", description="get sub country locations", response_model=List[schemas.Location])
async def read_sub_country_children(id: int, search:str=None, value:str=None, skip:int=0, limit:int=100, db: Session=Depends(get_db)):
    return await crud.read_sub_country_children(id, skip, limit, search, value, db)

@router3.patch("/{id}", description="update sub country", response_model=schemas.SubCountry)
async def update_sub_country(id: int, payload: schemas.UpdateSubCountry, db: Session=Depends(get_db)):
    return await crud.update_sub_country(id, payload, db)

@router3.delete("{id}", description="delete sub country", status_code = status.HTTP_202_ACCEPTED)
async def delete_sub_country(ids: List[int], db: Session=Depends(get_db)):
    return await crud.delete_sub_country(ids, db)
