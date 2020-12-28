from fastapi import APIRouter, Depends, HTTPException, status, Response
from . import crud, schemas, models
from sqlalchemy.orm import Session
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create about_us block(s)", response_model = schemas.AboutUs)
async def create_about_us(payload: schemas.CreateAboutUs, db: Session = Depends(get_db)):
    return await crud.create_about_us(payload, db)

@router.patch("/{id}", description="update about_us with id", response_model = schemas.AboutUs)
async def update_about_us(id:int, payload: schemas.UpdateAboutUs, db: Session = Depends(get_db)):
    return await crud.update_about_us(id, payload, db)

@router.delete("/", description="delete about_us", status_code = status.HTTP_202_ACCEPTED)
async def delete_about_us(ids: List[int], db: Session = Depends(get_db)):
    return await crud.delete_about_us(ids, db)

@router.get("/", description="read about_us", response_model = List[schemas.AboutUs])
async def read_about_us(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_about_us(search, value, db)

@router.get("/{id}", description="read faqs by id", response_model = schemas.AboutUs)
async def read_about_us_by_id(id: int, db: Session = Depends(get_db)):
    about_us = await crud.read_about_us_by_id(id, db)
    if not about_us:
        raise HTTPException(status_code=404)
    return about_us
