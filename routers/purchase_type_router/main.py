from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", description="create purchase type", response_model=schemas.PurchaseType, status_code=status.HTTP_201_CREATED)
async def create_purchase_type(payload: schemas.CreatePurchaseType, db: Session = Depends(get_db)):
    return await crud.create_purchase_type(payload, db)

@router.get("/", description="get purchase types", response_model=List[schemas.PurchaseType])
async def read_purchase_type(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_purchase_type(skip, limit, search, value, db)

@router.get("/{id}", description="get purchase type by id", response_model=schemas.PurchaseType)
async def read_purchase_type_by_id(id: int, db: Session = Depends(get_db)):
    purchase_type = await crud.read_purchase_type_by_id(id, db)
    if purchase_type is None:
        raise HTTPException(status_code=404)
    return purchase_type

@router.patch("/{id}", response_model=schemas.PurchaseType)
async def update_purchase_type(id: int, payload: schemas.UpdatePurchaseType, db: Session = Depends(get_db)):
    return await crud.update_purchase_type(id, payload, db)

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_purchase_type(id: int, db: Session = Depends(get_db)):
    return await crud.delete_purchase_type(id, db)