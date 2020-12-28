from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", description="create timeline", response_model=schemas.Timeline, status_code=status.HTTP_201_CREATED)
async def create_timeline(payload: schemas.CreateTimeline, db: Session = Depends(get_db)):
    return await crud.create_timeline(payload, db)

@router.get("/", description="get timeline", response_model=List[schemas.Timeline])
async def read_timeline(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_timeline(skip, limit, search, value, db)

@router.get("/{id}", description="get timeline by id", response_model=schemas.Timeline)
async def read_timeline_by_id(id: int, db: Session = Depends(get_db)):
    timeline = await crud.read_timeline_by_id(id, db)
    if timeline is None:
        raise HTTPException(status_code=404)
    return timeline

@router.patch("/{id}", description="update timeline", response_model=schemas.Timeline)
async def update_timeline(id: int, payload: schemas.UpdateTimeline, db: Session = Depends(get_db)):
    return await crud.update_timeline(id, payload, db)

@router.delete("/{id}", description="delete timeline", status_code=status.HTTP_202_ACCEPTED)
async def delete_timeline(id: int, db: Session = Depends(get_db)):
    return await crud.delete_timeline(id, db)