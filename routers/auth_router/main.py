from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from ..users_router.crud import read_user_by_id
from main import get_db, oauth2_scheme
from sqlalchemy.orm import Session
from . import crud, schemas, models
from typing import List
import utils, jwt

router = APIRouter()

@router.post("/", description="authenticate user details", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db: Session = Depends(get_db)):
    return await crud.authenticate(payload, db)

@router.post("/logout", description="log user out/revoke user access")
async def logout(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.revoke_token(payload, db)

@router.post("/refresh", description="refresh user access/refresh tokens", response_model=schemas.Token)
async def refresh_token(payload: schemas.Token, db: Session = Depends(get_db)):
    return await crud.refresh_token(payload, db)

@router.get("/", response_model=schemas.User)
async def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if await crud.is_token_blacklisted(token, db):
        raise HTTPException(status_code=401, detail="access unauthorised")
    try:
        token_data = utils.decode_token(data=token)
        if token_data:
            del token_data['exp']
            return await read_user_by_id(token_data['id'], db)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

@router.post("/request", description="authenticate user details")
async def request_password_reset(payload: schemas.Email, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    code = await crud.request_password_reset(payload, db, background_tasks)
    if code is None:
        raise HTTPException(status_code=417, detail="failed to generate reset code for user")
    return code