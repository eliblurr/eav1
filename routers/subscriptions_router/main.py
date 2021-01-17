from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys

from main import get_db
import utils

router = APIRouter()

# verify seller
# sho product on store homepage[sell view count]
# top product[push product to top of list][sell view count]
# purchase subscription
# ad subscription[view count][time_based]

# @router.post("/", status_code=status.HTTP_201_CREATED, description="create new subscription",response_model = schemas.Subscription )
# async def create_subscription(payload: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
#     return await crud.create_subscription(payload, db)

# @router.delete("/{id}", description="delete subscription_type with id")
# async def delete_subscription(id: int, db: Session = Depends(get_db)):
#     if not await crud.delete_subscription(id, db):  
#         raise HTTPException( status_code=400)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.patch("/{id}", status_code=status.HTTP_200_OK, description="update subscription_type details with id", response_model=schemas.Subscription)
# async def update_subscription(id: int, payload: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
#     return await crud.update_subscription(id, payload, db)

# @router.get("/", status_code=status.HTTP_200_OK, description="get/search for subscription_type", response_model=List[schemas.Subscription])
# async def read_subscription(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
#     return await crud.read_subscription(skip, limit, search, value, db)

# @router.get("/{id}", status_code=status.HTTP_200_OK, description="get subscription_type by id", response_model=schemas.Subscription)
# async def read_subscription_by_id(id: int, db: Session = Depends(get_db)):
#     subscription = await crud.read_subscription_by_id(id, db)
#     if not subscription:
#         raise HTTPException(status_code=404)
#     return subscription


