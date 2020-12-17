from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.PaymentType)
async def create_payment_type(payload: schemas.CreatePaymentType, db: Session = Depends(get_db)):
    return await crud.create_payment_type(payload, db)

@router.get("/", response_model=List[schemas.PaymentType])
async def read_payment_type(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_payment_type(skip, limit, search, value, db)

@router.get("/{id}", response_model=schemas.PaymentType)
async def read_payment_type_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.read_payment_type_by_id(id, db)

@router.patch("/{id}", response_model=schemas.PaymentType)
async def update_payment_type(id: int, payload: schemas.UpdatePaymentType, db: Session = Depends(get_db)):
    return await crud.update_payment_type(id, payload, db)

@router.delete("/{id}")
async def delete_payment_type(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_payment_type(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)