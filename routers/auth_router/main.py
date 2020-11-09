from fastapi import APIRouter, Depends, HTTPException
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

#authenticate/login
@router.post("/authenticate", response_model=schemas.Token)
async def authenticate(payload: schemas.UserBase, db: Session = Depends(get_db)):
    print(payload.dict())
    user = await crud.get_user_by_email(payload.email, db)
    if not user:
        raise HTTPException( status_code=404, detail="user not found")

    if user.auth_type.title == 'local':
        if await crud.verify_password(db, payload.password, user.password):
            access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
            return {'access_token': access_token, "token_type": "Bearer"}
        else:
            raise HTTPException( status_code=404, detail="failed to authenticate, check password")
            
    access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
    return {'access_token': access_token, "token_type": "Bearer"}

#get current user
@router.get("/current_user", response_model=schemas.User)
async def get_current_user(db: Session = Depends(get_db), payload : dict = Depends(utils.verify_token) ):
    try:
        if payload:
            return payload
        raise HTTPException(status_code=404, detail="user not found")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
   
# user registration
@router.post("/create")
async def create_users(payload:schemas.UserCreate, db: Session = Depends(get_db)):
    user = await crud.create_user(payload,db)
    if not user: 
        raise HTTPException(status_code=404, detail="could not create user" )
    return user

# delete user
@router.delete("/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return await crud.delete_user(user, db)

# get user by id
@router.get("/{id}")
async def read_user(id: int,db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return user

#read users
@router.get("/")
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None,):
    return await crud.get_users(db,skip,limit,search,value)

# update user info
@router.patch("/update/{id}")
async def update_user(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return await crud.update_user_info(id,payload,db)

# reset password
@router.post("/gen_reset_token")
async def gen_reset_token(email: str, db: Session = Depends(get_db)):
    user = await crud.get_user_by_email(email,db)
    if not user:
        raise HTTPException(status_code=404, detail="{} was not found".format(email))
    return await crud.add_reset_token(db,user)

@router.post("/verify_token/{id}")
async def verify_token(token: str, id: int, db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(id,db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return await crud.verify_reset_token(db,token,user)

@router.patch("/update_password/{id}")
async def update_password(payload: schemas.ResetPassword, id: int, db: Session = Depends(get_db)):
    return await crud.update_password(db,id,payload)

@router.get("/token/refresh")
async def refresh_token(user: schemas.User = Depends(get_current_user), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    await crud.create_revoked_token(db,token)
    # blacklist old token the create new one
    print(user)
    access_token = utils.create_access_token(data = user, expires_delta=access_token_expires)
    return {'access_token': access_token, "token_type": "Bearer"}

    # access_token= utils.create_access_token(
    #     data={"sub": user.username}, expires_delta=timedelta(minutes=15)
    # )
    # access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
    # return {'access_token': access_token, "token_type": "Bearer"}
    # data = payload.dict(), expires_delta=access_token_expires
    # return {"access_token": access_token, "token_type": "bearer"}
