from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys

from main import get_db, oauth2_scheme
import utils

access_token_expires = timedelta(minutes=30)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new announcement", response_model=schemas.Announcement)
async def create_announcement(payload: schemas.CreateAnnouncement, db: Session = Depends(get_db)):
    return await crud.create_announcement(payload, db)

@router.patch("/{id}", description="update announcement", response_model=schemas.Announcement)
async def update_announcement(id:int, payload: schemas.UpdateAnnouncement, db: Session = Depends(get_db)):
    return await crud.update_announcement(id, payload, db)

@router.delete("/", description="delete announcement")
async def delete_announcement(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_announcement(id, db):  
        raise HTTPException( status_code=500, detail="Operation failed")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="read announcements", response_model=List[schemas.Announcement])
async def read_announcement(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_announcement(search, value, db)

@router.get("/{id}", description="read announcement", response_model=schemas.Announcement)
async def read_announcement_by_id(id: int, db: Session = Depends(get_db)):
    announcement = await crud.read_announcement_by_id(id, db)
    if announcement is None:
        raise HTTPException(status_code=404)
    return announcement

@router.get("/randomize/announcement", description="read random announcement")
async def read_random_announcement(db: Session = Depends(get_db)):
    return await crud.read_random_announcement(db)