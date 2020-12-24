from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db
import utils
import sys

router = APIRouter()

@router.post("/", description="create new event", response_model= schemas.Event)
async def create_event(payload: schemas.CreateEvent = Depends(schemas.CreateEvent.as_form), images: List[UploadFile] = File(...), db: Session=Depends(get_db)):
    return await crud.create_event(payload, images, db)

@router.get("/", description="get/search events", response_model= List[schemas.Event])
async def read_event(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_event(skip, limit, search, value, db)

@router.get("/{id}", description="get event by id", response_model = schemas.Event)
async def read_event_by_id(id: int, db: Session = Depends(get_db)):
    event = await crud.read_event_by_id(id, db)
    if event is None:
        raise HTTPException(status_code=404)
    return event

@router.get("/{id}/items", description="get/search event", response_model = schemas.EventItems)
async def read_event_products(id: int,skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_event_products(id, skip, limit, search, value, db)

@router.patch("/{id}", description="update event details", response_model = schemas.Event)
async def update_event(id: int, payload: schemas.UpdateEvent, db: Session = Depends(get_db)):
    return await crud.update_event(id, payload, db)

@router.delete("/{id}", description="delete event by id")
async def delete_event(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_event(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}/items", description="add product to event with id value", response_model = schemas.Event)
async def add_item_to_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_item_to_event(id, payload, db)

@router.delete("/{id}/items", description="remove product to event with id value", response_model = schemas.Event)
async def remove_item_from_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_item_from_event(id, payload, db)

@router.patch("/{id}/images", description="add image to event", response_model = schemas.Event)
async def add_image_to_event(id: int, images: List[UploadFile] = File(...),db: Session = Depends(get_db)):
    return await crud.add_image_to_event(id, images, db)

@router.delete("/images/{id}", description="remove image for event")
async def remove_image_from_event(id: int, db: Session = Depends(get_db)):
    if not await crud.remove_image_from_event(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)