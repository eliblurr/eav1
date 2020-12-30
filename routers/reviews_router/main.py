from fastapi import APIRouter, Depends, HTTPException, Response, status
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

@router.post("/{product_id}/users/{user_id}", description="create new review", response_model=schemas.Reviews)
async def create_review(payload: schemas.ReviewsCreate, product_id: int, user_id: int, db: Session = Depends(get_db)):
    return await crud.create_review(payload, product_id, user_id, db)

@router.get("/{id}", description="get review", response_model = schemas.Reviews)
async def read_review_by_id(id: int, db: Session = Depends(get_db)):
    review = await crud.read_review_by_id(id, db)
    if review is None:
        raise HTTPException(status_code=404)
    return review

# @router.get("/products/{id}", description="get review", response_model = List[schemas.Reviews])
# async def read_product_reviews(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return await crud.read_product_reviews(id, skip, limit, db)

@router.get("/{product_id}/users/{user_id}", description="get user review of product", response_model = schemas.Reviews)
async def read_user_product_review(product_id: int, user_id: int, db: Session = Depends(get_db)):
    review = await crud.read_user_product_review(product_id, user_id, db)
    if review is None:
        raise HTTPException(status_code=404)
    return review

@router.delete("/{id}", description="create new review")
async def delete_review(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_review(id, db):
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{product_id}/users/{user_id}", description="get user review of product", response_model = List[schemas.Reviews])
async def delete_user_product_review(product_id: int, user_id: int, db: Session = Depends(get_db)):
    if not await crud.delete_user_product_review(product_id, user_id, db):
        raise HTTPException(status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}", description="create new review", response_model = schemas.Reviews)
async def update_review_by_id(id: int, payload:schemas.ReviewsUpdate, db: Session = Depends(get_db)):
    return await crud.update_review(id, payload, db)
