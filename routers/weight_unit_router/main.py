from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db
import sys

router = APIRouter()

@router.post("/", description="create new weight unit", response_model= schemas.WeightUnit)
async def create_weight_unit( payload: schemas.CreateWeightUnit, db: Session = Depends(get_db) ):
    return await crud.create_weight_unit(payload, db)

@router.get("/", description="get/search weight unit", response_model= List[schemas.WeightUnit])
async def read_weight_unit(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_weight_unit(skip, limit, search, value, db)

@router.get("/{id}", description="get weight unit by id", response_model = schemas.WeightUnit)
async def read_weight_unit_by_id(id: int, db: Session = Depends(get_db)):
    weight_unit = await crud.read_weight_unit_by_id(id, db)
    if weight_unit is None:
        raise HTTPException(status_code=404)
    return weight_unit

@router.patch("/{id}", description="update weight unit details", response_model = schemas.WeightUnit)
async def update_weight_unit(id: int, payload: schemas.UpdateWeightUnit, db: Session = Depends(get_db)):
    return await crud.update_weight_unit(id, payload, db)

@router.delete("/{id}", description="delete currency by id", status_code = status.HTTP_202_ACCEPTED)
async def delete_weight_unit(id: int, db: Session = Depends(get_db)):
    return await crud.delete_weight_unit(id, db)