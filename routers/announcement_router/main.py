from fastapi import APIRouter, Depends, HTTPException, status, Response
from . import crud, schemas,models
from sqlalchemy.orm import Session
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new announcement", response_model=schemas.Announcement)
async def create_announcement(payload: schemas.CreateAnnouncement, db: Session = Depends(get_db)):
    return await crud.create_announcement(payload, db)

@router.patch("/{id}", description="update announcement", response_model=schemas.Announcement)
async def update_announcement(id:int, payload: schemas.UpdateAnnouncement, db: Session = Depends(get_db)):
    return await crud.update_announcement(id, payload, db)

@router.delete("/", description="delete announcement", status_code = status.HTTP_202_ACCEPTED)
async def delete_announcement(id: int, db: Session = Depends(get_db)):
    return await crud.delete_announcement(id, db)

@router.get("/", description="read announcements", response_model=List[schemas.Announcement])
async def read_announcement(skip:int = 0, limit:int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_announcement(skip, limit, search, value, db)

@router.get("/{id}", description="read announcement by id", response_model=schemas.Announcement)
async def read_announcement_by_id(id: int, db: Session = Depends(get_db)):
    announcement = await crud.read_announcement_by_id(id, db)
    if announcement is None:
        raise HTTPException(status_code=404)
    return announcement

@router.get("/_/random", description="read random announcement", response_model=schemas.Announcement)
async def read_random_announcement(db: Session = Depends(get_db)):
    return await crud.read_random_announcement(db)