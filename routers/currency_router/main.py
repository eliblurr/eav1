from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
import utils
import sys

router = APIRouter()

@router.post("/", description="create new currency", response_model= schemas.Currency)
async def create_currency( payload: schemas.CreateCurrency, db: Session = Depends(get_db) ):
    return await crud.create_currency(payload, db)

@router.get("/", description="get/search currency", response_model= List[schemas.Currency])
async def read_currency(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_currency(skip, limit, search, value, db)

@router.get("/{id}", description="get currency by id", response_model = schemas.Currency)
async def read_category_by_id(id: int, db: Session = Depends(get_db)):
    currency = await crud.read_currency_by_id(id, db)
    if currency is None:
        raise HTTPException(status_code=404)
    return currency

@router.patch("/{id}", description="update currency details", response_model = schemas.Currency)
async def update_currency(id: int, payload: schemas.UpdateCurrency, db: Session = Depends(get_db)):
    return await crud.update_currency(id, payload, db)

@router.delete("/{id}", description="delete currency by id")
async def delete_currency(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_currency(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)