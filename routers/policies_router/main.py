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

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new policy", response_model = List[schemas.CreatePolicies])
async def create_policies(payload: List[schemas.CreatePolicies], db: Session = Depends(get_db)):
    return await crud.create_policies(payload, db)

@router.patch("/{id}", description="update policy with id", response_model=schemas.Policies)
async def update_policy(id:int, payload: schemas.UpdatePolicies, db: Session = Depends(get_db)):
    return await crud.update_policy(id, payload, db)

@router.delete("/", description="delete policies")
async def delete_policy(ids: List[int], db: Session = Depends(get_db)):
    if not await crud.delete_policy(ids, db):  
        raise HTTPException( status_code=404)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="read policies", response_model = List[schemas.Policies])
async def read_policies(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_policies(search, value, db)

@router.get("/{id}", description="read policy by id", response_model = schemas.Policies)
async def read_policy_by_id(id: int, db: Session = Depends(get_db)):
    policy = await crud.read_policy_by_id(id, db)
    if not policy:
        raise HTTPException(status_code = 404)
    return policy
