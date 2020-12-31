from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/products/{product_id}/users/{user_id}", description="create new review", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
async def create_review(payload: schemas.CreateReview, product_id: int, user_id: int, db: Session=Depends(get_db)):
    return await crud.create_review(payload, product_id, user_id, db)

@router.get("/{id}", description="read review", response_model=schemas.Review)
async def read_review_by_id(id: int, db: Session=Depends(get_db)):
    review = await crud.read_review_by_id(id, db)
    if review is None:
        raise HTTPException(status_code=404)
    return review

@router.get("/products/{product_id}/users/{user_id}", description="get user review of product", response_model = schemas.Review)
async def read_user_product_review(product_id: int, user_id: int, db: Session=Depends(get_db)):
    return await crud.read_user_product_review(product_id, user_id, db)

@router.patch("/{id}/users/{author_id}", description="update review", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Review)
async def update_review(id: int, author_id:int, payload:schemas.UpdateReview, db: Session=Depends(get_db)):
    return await crud.update_review(id, author_id, payload, db)

@router.delete("/{id}/users/{author_id}", description="delete review", status_code=status.HTTP_202_ACCEPTED)
async def delete_review(id: int, author_id:int,db: Session=Depends(get_db)):
    return await crud.delete_review(id, author_id, db)