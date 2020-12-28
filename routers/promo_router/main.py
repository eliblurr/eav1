from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas, models
from main import get_db
from typing import List

router = APIRouter()

@router.post("/", description="create promo voucher", status_code=status.HTTP_201_CREATED, response_model = schemas.PromoVoucher)
async def create_promo(payload: schemas.CreatePromoVoucher, db: Session = Depends(get_db)):
    return await crud.create_promo(payload, db)

@router.get("/", description="get promo vouchers", status_code=status.HTTP_200_OK, response_model = List[schemas.PromoVoucher])
async def read_promo(start: float = 0, end: float = 0, skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_promo(start, end, skip, limit, search, value, db)

@router.get("/{id}", description="get promo voucher by id", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def read_promo_by_id(id: int, db: Session = Depends(get_db)):
    promo = await crud.read_promo_by_id(id, db)
    if not promo:
        raise HTTPException( status_code=404)
    return promo

@router.patch("/{id}", description="update promo voucher", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def update_promo(id: int, payload:schemas.UpdatePromoVoucher, db: Session = Depends(get_db)):
    return await crud.update_promo(id, payload, db)

@router.patch("/{id}/users/{user_id}", description="assign promo voucher to user", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def assign_promo(id: int, user_id: int, db: Session = Depends(get_db)):
    return await crud.assign_promo(id, user_id, db)

@router.patch("/unassign/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PromoVoucher)
async def unassign_promo(id: int, db: Session = Depends(get_db)):
    return await crud.unassign_promo(id, db)

@router.delete("/{id}", description="delete promo voucher by id", status_code=status.HTTP_202_ACCEPTED)
async def delete_promo(id: int, db: Session = Depends(get_db)):
    return await crud.delete_promo(id, db) 

