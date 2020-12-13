from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import crud, schemas
from main import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Delivery)
async def add_delivery(payload: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    return await crud.add_delivery(payload,db)

@router.get("/", response_model=List[schemas.Delivery])
async def get_delivery(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_delivery(skip,limit,search,value,db)

@router.get("/{id}", response_model=schemas.Delivery)
async def read_delivery_by_id(id: int, db: Session = Depends(get_db)):
    delivery = await crud.read_delivery_by_id(id, db)
    if not delivery:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return delivery

@router.patch("/{id}", response_model=schemas.Delivery)
async def update_delivery(id: int, payload: schemas.DeliveryUpdate, db: Session = Depends(get_db)):
    return await update_delivery(id, payload, db)

@router.delete("/{id}")
async def delete_delivery(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_delivery(id, db):
        raise HTTPException(status_code=400, detail="operation failed")
    return Response(status_code=status.HTTP_204_NO_CONTENT)