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

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new T&C block", response_model = List[schemas.CreateTC])
async def create_tC_blocks(payload: List[schemas.CreateTC], db: Session = Depends(get_db)):
    return await crud.create_tC_blocks(payload, db)

@router.patch("/{id}", description="update tC block(s)",response_model = schemas.TC)
async def update_tC_blocks(id:int, payload: schemas.UpdateTC, db: Session = Depends(get_db)):
    return await crud.update_tC_blocks(id, payload, db)

@router.delete("/", description="delete tC block(s)")
async def delete_tC_block(ids: List[int], db: Session = Depends(get_db)):
    if not await crud.delete_tC_block(ids, db):
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="read TC]", response_model = List[schemas.TC])
async def read_tC_blocks(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_tC_blocks(search, value, db)

@router.get("/{id}", description="read TC by id", response_model = schemas.TC)
async def read_tC_block_by_id(id: int, db: Session = Depends(get_db)):
    t_c = await crud.read_tC_block_by_id(id, db)
    if t_c is None:
        raise HTTPException(status_code=404)
    return t_c