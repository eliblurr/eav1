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

from ..users_router.main import get_current_user

#authenticate/login
@router.post("/", response_model=schemas.Token, description="")
async def authenticate(payload: schemas.UserBase, db: Session = Depends(get_db)):
    print(payload.dict())
#     user = await crud.get_user_by_email(payload.email, db)
#     if not user:
#         raise HTTPException( status_code=404, detail="user not found")

#     if user.auth_type.title == 'local':
#         if await crud.verify_password(db, payload.password, user.password):
#             access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
#             return {'access_token': access_token, "token_type": "Bearer"}
#         else:
#             raise HTTPException( status_code=404, detail="failed to authenticate, check password")
            
#     access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
#     return {'access_token': access_token, "token_type": "Bearer"}

# reset password
@router.post("/get_reset_token", description="generate password reset token")
async def gen_reset_token(email: str, db: Session = Depends(get_db)):
    print('sd')
#     user = await crud.get_user_by_email(email,db)
#     if not user:
#         raise HTTPException(status_code=404, detail="{} was not found".format(email))
#     return await crud.add_reset_token(db,user)

# 
@router.post("/verify_reset_token/{id}", description="verify reset token")
async def verify_token(token: str, id: int, db: Session = Depends(get_db)):
        print('sd')
#     user = await crud.get_user_by_id(id,db)
#     if not user:
#         raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
#     return await crud.verify_reset_token(db,token,user)

# 
@router.get("/refresh", description="refresh token")
async def refresh_token(user: schemas.User = Depends(get_current_user), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print('dd')
#     await crud.create_revoked_token(db,token)
#     # blacklist old token the create new one
#     print(user)
#     access_token = utils.create_access_token(data = user, expires_delta=access_token_expires)
#     return {'access_token': access_token, "token_type": "Bearer"}

#     # access_token= utils.create_access_token(
#     #     data={"sub": user.username}, expires_delta=timedelta(minutes=15)
#     # )
#     # access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
#     # return {'access_token': access_token, "token_type": "Bearer"}
#     # data = payload.dict(), expires_delta=access_token_expires
#     # return {"access_token": access_token, "token_type": "bearer"}

@router.get('/revoke', description="revoke refresh token")
def revoke_token():
    print('sd')
# /authenticate
# /get_user
# /refresh
# /revoke