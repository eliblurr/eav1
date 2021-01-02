from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import crud, schemas
from main import get_db
from typing import List

router = APIRouter()

@router.post("_options/", description="create delivery option", status_code=status.HTTP_201_CREATED, response_model=schemas.DeliveryOption)
async def create_delivery_option(payload: schemas.CreateDeliveryOption, db:Session=Depends(get_db)):
    return await crud.create_delivery_option(payload, db)

@router.get("_options/", description="read delivery options", response_model=List[schemas.DeliveryOption])
async def read_delivery_option(skip:int=0, limit:int=100, search:str=None, value:str=None, location_id:int=0, db:Session=Depends(get_db)):
    return await crud.read_delivery_option(skip, limit, search, value, location_id, db)

@router.get("_options/{id}", description="read delivery option by id", response_model=schemas.DeliveryOption)
async def read_delivery_by_id(id:int, db:Session=Depends(get_db)):
    delivery_option = await crud.read_delivery_option(id, db)
    if not delivery_option:
        raise HTTPException(status_code=404)
    return delivery_option

@router.patch("_options/{id}", description="update delivery option", response_model=schemas.DeliveryOption, status_code=status.HTTP_202_ACCEPTED)
async def update_delivery_option(id:int, payload:schemas.UpdateDeliveryOption, db:Session=Depends(get_db)):
    return await crud.update_delivery_option(id, payload, db)

@router.delete("_options/{id}", description="delete delivery option", status_code=status.HTTP_202_ACCEPTED)
async def delete_delivery_option(id:int, db:Session=Depends(get_db)):
    return await crud.delete_delivery_option(id, db)

@router.post("/", description="create delivery", status_code=status.HTTP_201_CREATED, response_model=schemas.Delivery)
async def create_delivery(payload:schemas.CreateDelivery, db:Session=Depends(get_db)):
    return await crud.create_delivery(payload, db)

@router.get("/", description="read delivery", response_model=List[schemas.Delivery])
async def read_delivery(skip:int=0, limit:int=100, search:str=None, value:str=None, db:Session=Depends(get_db)):
    return await crud.read_delivery(skip, limit, search, value, db)

@router.get("/{id}", description="read delivery by id", response_model=schemas.Delivery)
async def read_delivery_by_id(id:int, db:Session=Depends(get_db)):
    delivery = await crud.read_delivery_by_id(id, db)
    if not delivery:
        raise HTTPException(status_code=404)
    return delivery

@router.patch("/{id}", description="update delivery details", response_model=schemas.Delivery, status_code=status.HTTP_202_ACCEPTED)
async def update_delivery(id:int, payload:schemas.UpdateDelivery, db:Session=Depends(get_db)):
    return await crud.update_delivery(id, payload, db)

@router.delete("/{id}", description="delete delivery", status_code=status.HTTP_202_ACCEPTED)
async def delete_delivery(id:int, db:Session=Depends(get_db)):
    return await crud.delete_delivery(id, db)

@router.post("_timelines/{id}", description="create custom timeline for delivery", response_model=schemas.DeliveryTimeline, status_code=status.HTTP_201_CREATED)
async def create_delivery_timeline(id:int, payload:schemas.CreateDeliveryTimeline, db:Session=Depends(get_db)):
    return await crud.create_delivery_timeline(id, payload, db)

@router.put("/{id}/timelines/{timeline_id}", description="add or remove timeline from delivery timeline", status_code=status.HTTP_202_ACCEPTED)
async def toggle_timeline_delivery(id:int, timeline_id:int, db:Session=Depends(get_db)):
    return await crud.toggle_timeline_delivery(id, timeline_id, db)

@router.get("_timeline/{id}", description="read delivery timeline", response_model=List[schemas.DeliveryTimeline])
async def read_delivery_timeline(id:int, skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    return await crud.read_delivery_timeline(id, skip, limit, db)