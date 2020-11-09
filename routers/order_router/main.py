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

@router.post('/rental')
async def rent_product(payload: List[schemas.Rental], db: Session = Depends(get_db)):
    return payload

@router.post('/purchase')
async def rent_product(payload: List[schemas.Purchase], db: Session = Depends(get_db)):
    return payload

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
