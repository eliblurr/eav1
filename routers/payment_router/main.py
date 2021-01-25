from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", description="create payment", status_code=status.HTTP_201_CREATED, response_model=schemas.Payment)
async def create_payment(payload: schemas.CreatePayment, db: Session = Depends(get_db)):
    return await crud.create_payment(payload, db)

@router.get("/", description="read payments", response_model=List[schemas.Payment])
async def read_payment(skip: int=0, limit: int=100, search:str = None, value:str = None, start_amount:float=0, end_amount:float=0, user_id:int=0, db: Session = Depends(get_db)):
    return await crud.read_payment(skip, limit, search, value, start_amount, end_amount, user_id, db)

@router.get("/{id}", description="read payment by id", response_model=schemas.Payment)
async def read_payment_by_id(id: int, db: Session = Depends(get_db)):
    payment = await crud.read_payment_by_id(id, db)
    if not payment:
        raise HTTPException(status_code=404)
    return payment

@router.patch("/{id}", description="update payment", response_model=schemas.Payment, status_code = status.HTTP_202_ACCEPTED)
async def update_payment(id: int, payload: schemas.UpdatePayment, db: Session = Depends(get_db)):
    return await crud.update_payment(id, payload, db)

@router.delete("/{id}", description="delete payment", status_code = status.HTTP_202_ACCEPTED)
async def delete_payment(id: int, db: Session = Depends(get_db)):
    return await crud.delete_payment(id, db)
