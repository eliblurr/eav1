from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", description="create payment type", response_model=schemas.PaymentType, status_code=status.HTTP_201_CREATED)
async def create_payment_type(payload: schemas.CreatePaymentType, db: Session = Depends(get_db)):
    return await crud.create_payment_type(payload, db)

@router.get("/", description="get payment types", response_model=List[schemas.PaymentType])
async def read_payment_type(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_payment_type(skip, limit, search, value, db)

@router.get("/{id}", description="get payment type by id", response_model=schemas.PaymentType)
async def read_payment_type_by_id(id: int, db: Session = Depends(get_db)):
    payment_type = await crud.read_payment_type_by_id(id, db)
    if payment_type is None:
        raise HTTPException(status_code=404)
    return payment_type

@router.patch("/{id}", description="update payment type", response_model=schemas.PaymentType)
async def update_payment_type(id: int, payload: schemas.UpdatePaymentType, db: Session = Depends(get_db)):
    return await crud.update_payment_type(id, payload, db)

@router.delete("/{id}", description="delete payment type", status_code=status.HTTP_202_ACCEPTED)
async def delete_payment_type(id: int, db: Session = Depends(get_db)):
    return await crud.delete_payment_type(id, db)