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

from ..product_router.schemas import Product

router = APIRouter()

@router.post("/{user_id}/products/{product_id}" )
async def add_to_user_favorites(product_id: int, user_id: int, db: Session = Depends(get_db)):
    return await crud.add_to_user_favorites(product_id, user_id, db)

@router.get("/{user_id}", response_model=List[Product])
async def add_to_user_favorites(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await crud.get_user_favorites(user_id, skip, limit, db)

@router.delete("/{user_id}/products/{product_id}")
async def remove_from_user_favorites(product_id: int, user_id: int, db: Session = Depends(get_db)):
    return await crud.remove_from_user_favorites(product_id, user_id, db)

