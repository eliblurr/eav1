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

@router.post("/", response_model=schemas.Order)
async def create_order(payload: schemas.CreateOrder, db: Session = Depends(get_db)):
    return payload

@router.get("/", response_model=List[schemas.Order])
async def get_order(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return

@router.get("/{id}", response_model=schemas.Order)
async def get_order_by_id(id: int, db: Session = Depends(get_db)):
    return

@router.patch("/{id}", response_model=schemas.Order)
async def update_order(id: int, payload: schemas.UpdateOrder, db: Session = Depends(get_db)):
    return

@router.delete("/{id}")
async def delete_order():
    # if not await crud.delete_payment(id, db):
    #     raise HTTPException( status_code=500)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return


# make order
# - validate user[get usertype from token]
# cancel orer
# delete order
# - validate user[get usertype for token and check if user owns the product[admins can disable products]]
# rent products
# - validate user -> [get usertype from token -> validate payment -> [check if product quantity is >=] -> [create order for user -> update product details -> create scheduled job for when rental expires]]
# update rental period
# - update scheduled job [job id -> Type_UserID_product_ID]
# buy products
# - validate user -> [get usertype from token -> validate payment -> [check if product quantity is >=] -> [create order for user -> update product details]]
# read product[search]
# read product by id
