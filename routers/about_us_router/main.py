from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys

from main import get_db, oauth2_scheme
import utils

access_token_expires = timedelta(minutes=30)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new about us block", response_model = List[schemas.CreateAboutUs])
async def create_about_us(payload: List[schemas.CreateAboutUs], db: Session = Depends(get_db)):
    return await crud.create_about_us(payload, db)

@router.patch("/{id}", description="update faqs with id", response_model = schemas.AboutUs)
async def update_about_us(id:int, payload: schemas.UpdateAboutUs, db: Session = Depends(get_db)):
    return await crud.update_about_us(id, payload, db)

@router.delete("/", description="delete faqs")
async def delete_about_us(ids: List[int], db: Session = Depends(get_db)):
    if not await crud.delete_about_us(ids, db):  
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="read faqs", response_model = List[schemas.AboutUs])
async def read_about_us(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_about_us(search, value, db)

@router.get("/{id}", description="read faqs by id", response_model = schemas.AboutUs)
async def read_about_us_by_id(id: int, db: Session = Depends(get_db)):
    about_us = await crud.read_about_us_by_id(id, db)
    if not about_us:
        raise HTTPException(status_code=404)
    return about_us
