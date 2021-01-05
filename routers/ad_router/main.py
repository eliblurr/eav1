from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from . import crud, schemas, models
from sqlalchemy.orm import Session
from typing import List, Optional 
from main import get_db

router = APIRouter()
router2 = APIRouter()

@router.post("/", description="create ad", status_code=status.HTTP_201_CREATED, response_model=schemas.Ad)
async def create_ad(payload=Depends(schemas.CreateAd.as_form), images:List[UploadFile]=File(None), db:Session=Depends(get_db)):
    return await crud.create_ad(payload, images, db)

@router.get("/", description="read ads", response_model=List[schemas.Ad])
async def read_ads(skip:int=0, limit:int=100, search:str=None, value:str=None, location_id:int=0, db:Session=Depends(get_db)):
    return await crud.read_ads(skip, limit, search, value, location_id, db)

@router.get("/{id}", description="read ad by id", response_model=schemas.Ad)
async def read_ad_by_id(id:int, db:Session=Depends(get_db)):
    ad = await crud.read_ad_by_id(id, db)
    if not ad:
        raise HTTPException(status_code=404)
    return ad

@router.patch("/{id}", description="update ad", response_model=schemas.Ad, status_code=status.HTTP_202_ACCEPTED)
async def update_ad(id:int, payload:schemas.UpdateAd, db:Session=Depends(get_db)):
    return await crud.update_ad(id, payload, db)

@router.delete("/{id}", description="delete ad", status_code=status.HTTP_202_ACCEPTED)
async def delete_ad(id:int, db:Session=Depends(get_db)):
    return await crud.delete_ad(id, db)

@router.patch("/{id}/images", description="add ad image", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Ad)
async def add_image_ad(id:int, images:List[UploadFile]=File(...), db:Session=Depends(get_db)):
    return await crud.add_image_ad(id, images, db)

@router.delete("/{id}/images", description="remove ad image", status_code=status.HTTP_202_ACCEPTED)
async def remove_image_ad(id:int, db:Session=Depends(get_db)):
    return await crud.remove_image_ad(id, db)

@router.put("/{id}/locations", description="add location to ad", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Ad)
async def add_location_to_ad(id:int, location_ids:List[int], db:Session=Depends(get_db)):
    return await crud.add_location_to_ad(id, location_ids, db)

@router.delete("/{id}/locations", description="remove location from ad", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Ad)
async def remove_location_from_ad(id:int, location_ids:List[int], db:Session=Depends(get_db)):
    return await crud.remove_location_from_ad(id, location_ids, db)

@router2.post("/", description="create ad style", status_code=status.HTTP_201_CREATED, response_model=schemas.Style)
async def create_style(payload:schemas.CreateStyle, db:Session=Depends(get_db)):
    return await crud.create_style(payload, db)

@router2.get("/", description="read ad styles", response_model=List[schemas.Style])
async def read_styles(skip:int=0, limit:int=100, search:str=None, value:str=None, db:Session=Depends(get_db)):
    return await crud.read_styles(skip, limit, search, value, db)

@router2.get("/{id}", description="read ad style by id", response_model=schemas.Style)
async def read_style_by_id(id:int, db:Session=Depends(get_db)):
    style = await crud.read_style_by_id(id, db)
    if not style:
        raise HTTPException(status_code=404)
    return style

@router2.patch("/{id}", description="update ad style", response_model=schemas.Style, status_code=status.HTTP_202_ACCEPTED)
async def update_style(id:int, payload:schemas.UpdateStyle, db:Session=Depends(get_db)):
    return await crud.update_style(id, payload, db)

@router2.delete("/{id}", description="delete ad style", status_code=status.HTTP_202_ACCEPTED)
async def delete_style(id:int, db:Session=Depends(get_db)):
    return await crud.delete_style(id, db)