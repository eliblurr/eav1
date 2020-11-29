from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys
import traceback

from main import get_db, oauth2_scheme, settings
import utils

from services.email import simple_send, send_in_background

access_token_expires = timedelta(minutes=30)

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

@router.patch("/{id}/password", response_model=schemas.User)
async def update_password(id: int, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    return await crud.reset_password(id,payload,db)

# request password reset
@router.post("/request")
async def request_password_reset(background_tasks: BackgroundTasks):
    # import config
    print(type(settings.SECRET_KEY))
    print(type(settings.MAIL_USERNAME))
    print(type(settings.MAIL_PASSWORD))
    print(type(settings.MAIL_SERVER))
    print(type(settings.MAIL_TLS))
    print(type(settings.MAIL_FROM))
    # user = await crud.get_user_by_id(id, db)
    # if user is None:
    #     raise HTTPException(status_code=404)
    # try:
    await send_in_background(background_tasks)
    # await simple_send({'email':['elvissegbawu@gmail.com']})
    # raise HTTPException(status_code=200)
    # except:
    #     print(traceback.format_exc())
    #     raise HTTPException(status_code=500)

    # await simple_send(email: EmailSchema,subject: str, body: List[str])

    




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