from fastapi import APIRouter, Depends, HTTPException, status
from . import crud, schemas, models
from sqlalchemy.orm import Session
from main import get_db
from typing import List

router = APIRouter()

@router.post("/", description="create/register user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(payload: schemas.CreateUser, db: Session=Depends(get_db)):
    return await crud.create_user(payload, db)

@router.post("/verify_password", description="verify password")
async def verify_password(id: int, payload: schemas.ResetPassword, db: Session=Depends(get_db)):
    return await crud.verify_password(id, payload, db)

@router.get("/", description="read users", response_model=List[schemas.User])
async def read_users(skip:int=0, limit:int=100, search:str=None, value:str=None, db: Session=Depends(get_db)):
    return await crud.read_users(skip, limit, search, value, db)

@router.get("/{id}", description="get user by id", response_model=schemas.User)
async def read_user_by_id(id: int, db: Session=Depends(get_db)):
    user = await crud.read_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=404)
    return user

@router.patch("/{id}", description="update user details", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id:int, payload:schemas.UpdateUser, db:Session=Depends(get_db)):
    return await crud.update_user(id, payload, db)

@router.patch("/{id}/password", description="update user password", status_code=status.HTTP_202_ACCEPTED)
async def reset_password(id:int, payload: schemas.ResetPassword, db: Session=Depends(get_db)):
    return await crud.reset_password(id, payload, db)

@router.delete("/{id}", description="delete user", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(ids: List[int], db: Session=Depends(get_db)):
    return await crud.delete_user(ids, db)
 