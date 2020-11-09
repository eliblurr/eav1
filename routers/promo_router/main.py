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

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.PromoVoucher)
async def create_promo(payload: schemas.CreatePromoVoucher, db: Session = Depends(get_db)):
    return await crud.create_promo(payload, db)

@router.delete("/{id}")
async def delete_promo(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_promo(id, db):  
        raise HTTPException( status_code=500, detail="Operation failed")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", status_code=status.HTTP_200_OK, response_model = List[schemas.PromoVoucher])
async def get_promo_vouchers(start_amount: float = 0, end_amount: float = 0, skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_promo(db, start_amount, end_amount, skip, limit, search, value)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def get_promo_by_id(id: int, db: Session = Depends(get_db)):
    promo = await crud.read_promo_by_id(id, db)
    if not promo:
        raise HTTPException( status_code=404)
    return promo

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def update_promo_by_id(id: int, payload:schemas.UpdatePromoVoucher, db: Session = Depends(get_db)):
    return await crud.update_promo_by_id(id, payload, db)

@router.patch("/{id}/assign_to/{owner_id}", status_code=status.HTTP_200_OK)
async def assign_promo_voucher(id: int, owner_id: int, db: Session = Depends(get_db)):
    return await crud.assign_promo(id, owner_id, db)

@router.patch("/unassign/{id}", status_code=status.HTTP_200_OK)
async def unassign_promo_voucher(id: int, db: Session = Depends(get_db)):
    return await crud.unassign_promo(id, db)

