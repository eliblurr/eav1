from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile,Form
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys
from ..product_router.schemas import Product

from main import get_db, oauth2_scheme
import utils

router = APIRouter()

@router.post("/", description="create new event", response_model= schemas.Events)
async def create_event(payload: schemas.CreateEvents = Depends(schemas.CreateEvents.as_form), images: List[UploadFile] = File(...), db: Session= Depends(get_db)):
    return await crud.create_event(payload, images, db)

@router.delete("/{id}", description="delete event by id")
async def delete_event(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_event(id, db):
        raise HTTPException(status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.get("/", description="get/search events", response_model= List[schemas.Events])
async def read_event(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_event(skip, limit, search, value, db)

@router.get("/{id}", description="get event by id", response_model=schemas.Events)
async def read_event_by_id(id: int, db: Session = Depends(get_db)):
    event = await crud.read_event_by_id(id, db)
    if event is None:
        raise HTTPException(status_code=404)
    return event
 
@router.get("/{id}/products", description="get products in events with path id value", response_model=List[Product])
async def read_event_products(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await crud.read_event_products(id, skip, limit, db)

@router.patch("/{id}", description="update event details", response_model=schemas.Events)
async def update_event_details(id: int, payload: schemas.UpdateEvents, db: Session = Depends(get_db)):
    return await crud.update_event_details(id, payload, db)

@router.patch("/{id}/addproducts", description="add product to event with id value", response_model=schemas.Events)
async def add_item_to_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_item_to_event(id, payload, db)

@router.patch("/{id}/removeproducts", description="remove product from event with id value", response_model=schemas.Events)
async def remove_item_from_event(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_item_from_event(id, payload, db)

@router.patch("/{id}/addimages", description="add image for event", response_model = schemas.Events)
async def add_image_to_event(id: int, image: UploadFile = File(...),db: Session = Depends(get_db)):
    return await crud.add_image_to_event(id, image, db)

@router.delete("/{id}/images/{image_id}", description="remove image for event", response_model = schemas.Events)
async def remove_image_from_event(id: int, image_id: int, db: Session = Depends(get_db)):
    return await crud.remove_image_from_event(id, image_id, db)
