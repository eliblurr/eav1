from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Payment)
async def create_payment(payload: schemas.CreatePayment, db: Session = Depends(get_db)):
    return await crud.create_payment(payload, db)

@router.get("/", response_model=List[schemas.Payment])
async def read_payment(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_payment(skip, limit, search, value, db)

@router.get("/{id}", response_model=schemas.Payment)
async def read_payment_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.read_payment_by_id(id, db)

@router.get("/amount/filter", response_model=List[schemas.Payment])
async def filter_payment(skip: int=0, limit: int=100, lower_boundary:float = 0, upper_boundary:float = 0, db: Session = Depends(get_db)):
    return await crud.filter_payment(skip, limit, lower_boundary, upper_boundary, db)

@router.patch("/{id}", response_model=schemas.Payment)
async def update_payment(id: int, payload: schemas.UpdatePayment, db: Session = Depends(get_db)):
    return await crud.update_payment(id, payload, db)

@router.delete("/{id}")
async def delete_payment(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_payment(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
