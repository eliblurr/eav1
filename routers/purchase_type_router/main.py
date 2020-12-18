from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.PurchaseType)
async def create_purchase_type(payload: schemas.CreatePurchaseType, db: Session = Depends(get_db)):
    return await crud.create_purchase_type(payload, db)

@router.get("/", response_model=List[schemas.PurchaseType])
async def read_purchase_type(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_purchase_type(skip, limit, search, value, db)

@router.get("/{id}", response_model=schemas.PurchaseType)
async def read_purchase_type_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.read_purchase_type_by_id(id, db)

@router.patch("/{id}", response_model=schemas.PurchaseType)
async def update_purchase_type(id: int, payload: schemas.UpdatePurchaseType, db: Session = Depends(get_db)):
    return await crud.update_purchase_type(id, payload, db)

@router.delete("/{id}")
async def delete_purchase_type(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_purchase_type(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)