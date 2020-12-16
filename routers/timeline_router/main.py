from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Timeline)
async def create_timeline(payload: schemas.CreateTimeline, db: Session = Depends(get_db)):
    return await crud.create_timeline(payload, db)

@router.get("/", response_model=List[schemas.Timeline])
async def read_timeline(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_timeline(skip, limit, search, value, db)

@router.get("/{id}", response_model=schemas.Timeline)
async def read_timeline_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.read_timeline_by_id(id, db)

@router.patch("/{id}", response_model=schemas.Timeline)
async def update_timeline(id: int, payload: schemas.UpdateTimeline, db: Session = Depends(get_db)):
    return await crud.update_timeline(id, payload, db)

@router.delete("/{id}")
async def delete_timeline(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_timeline(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)