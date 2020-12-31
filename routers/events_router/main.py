from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db
import utils
import sys

router = APIRouter()

@router.post("/", description="create new event", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
async def create_event(payload=Depends(schemas.CreateEvent.as_form), images: List[UploadFile] = File(...), db: Session=Depends(get_db)):
    return await crud.create_event(payload, images, db)

@router.get("/", description="read events", response_model= List[schemas.Event])
async def read_event(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_event(skip, limit, search, value, db)

@router.get("/{id}", description="read event by id", response_model=schemas.Event)
async def read_event_by_id(id: int, db: Session = Depends(get_db)):
    event = await crud.read_event_by_id(id, db)
    if event is None:
        raise HTTPException(status_code=404)
    return event

@router.get("/{id}/products", description="read event products", response_model=List[schemas.Product])
async def read_event_products(id: int,skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_event_products(id, skip, limit, search, value, db)

@router.patch("/{id}", description="update event", response_model=schemas.Event, status_code=status.HTTP_202_ACCEPTED)
async def update_event(id: int, payload: schemas.UpdateEvent, db: Session = Depends(get_db)):
    return await crud.update_event(id, payload, db)

@router.patch("/{id}/images", description="add image to event", response_model=schemas.Event, status_code=status.HTTP_202_ACCEPTED)
async def add_event_image(id: int, images: List[UploadFile] = File(...),db: Session = Depends(get_db)):
    return await crud.add_event_image(id, images, db)

@router.patch("/{id}/products", description="add product to event", response_model = schemas.Event, status_code=status.HTTP_202_ACCEPTED)
async def add_item_to_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_item_to_event(id, payload, db)

@router.delete("/{id}", description="delete event", status_code=status.HTTP_202_ACCEPTED)
async def delete_event(id: int, db: Session = Depends(get_db)):
    return await crud.delete_event(id, db)

@router.delete("/{id}/products", description="remove product from event", status_code=status.HTTP_202_ACCEPTED)
async def remove_product_from_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_product_from_event(id, payload, db)

@router.delete("/images/{id}", description="delete event image", status_code=status.HTTP_202_ACCEPTED)
async def remove_event_image(id: int, db: Session = Depends(get_db)):
    return await crud.remove_event_image(id, db)