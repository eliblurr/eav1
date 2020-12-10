from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks
from services.email import simple_send, send_in_background
from main import get_db, oauth2_scheme, settings
from pydantic import UUID4, EmailStr
from . import crud, schemas,models
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import traceback
import utils
import jwt
import sys

router = APIRouter()

# user registration
@router.post("/",response_model=schemas.User)
async def create_users(payload:schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(payload,db)

# delete user
@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_user(id, db):
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# get user by id
@router.get("/{id}", description="get user by id", response_model=schemas.User)
async def read_user(id: int,db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return user

#read users
@router.get("/", description="get all users", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None,):
    return await crud.get_users(db,skip,limit,search,value)

# update user info
@router.patch("/update/{id}", response_model=schemas.User)
async def update_user(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    return await crud.update_user(id,payload,db)

# verify user password
@router.post("/verify/password")
async def verify_password(id: int, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.verify_password(id, payload, db)

# update user password
@router.patch("/{id}/password", status_code=status.HTTP_202_ACCEPTED)
async def update_password(id: int, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.reset_password(id,payload,db)