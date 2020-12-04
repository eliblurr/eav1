from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from main import get_db, oauth2_scheme
from pydantic import UUID4, EmailStr
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
import utils
import jwt
import sys

router = APIRouter()

@router.post("/", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db: Session = Depends(get_db)):
    return await crud.authenticate(payload, db)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.refresh_token(payload, db)

@router.get("/")
async def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    res = await crud.is_token_blacklisted(token, db)

    if res:
        raise HTTPException(status_code=401, detail="access unauthorised")

    try:
        token_data = utils.decode_access_token(data=token)
        if token_data:
            del token_data['exp']
            return token_data
        
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})

    except jwt.exceptions.DecodeError as e:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

@router.post("/request")
async def request_password_reset(payload: schemas.Email, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    code = await crud.request_password_reset(payload, db, background_tasks)
    if code is None:
        raise HTTPException(status_code=417, detail="failed to generate reset code for user")
    return code