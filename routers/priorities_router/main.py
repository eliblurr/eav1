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

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new priority", response_model = schemas.Priority)
async def create_proirity(payload: schemas.PriorityCreate, db: Session = Depends(get_db)):
    return await crud.create_priority(payload, db)

@router.delete("/{id}", description="delete priority with id")
async def delete_priority(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_priority(id, db):  
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", status_code=status.HTTP_200_OK, description="update priority details with id")
async def update_priority(id: int, payload: schemas.PriorityUpdate, db: Session = Depends(get_db)):
    return await crud.update_priority(id, payload, db)

@router.get("/", status_code=status.HTTP_200_OK, description="get/search for priorities", response_model=List[schemas.Priority])
async def read_priorities(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_priorities(skip, limit, search, value, db)

@router.get("/{id}", status_code=status.HTTP_200_OK, description="get priority by id", response_model = schemas.Priority)
async def read_priority_by_id(id: int, db: Session = Depends(get_db)):
    priority = await crud.read_priority_by_id(id,db)
    if not priority:
        raise HTTPException(status_code=404)
    return priority
