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

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new faqs", response_model = List[schemas.CreateFAQs])
async def create_faqs(payload: List[schemas.CreateFAQs], db: Session = Depends(get_db)):
    return await crud.create_faqs(payload, db)

@router.patch("/{id}", description="update faqs with id")
async def update_faqs(id:int, payload: schemas.UpdateFAQs, db: Session = Depends(get_db)):
    return await crud.update_faq(id, payload, db)

@router.delete("/", description="delete faqs")
async def delete_faqs(ids: List[int], db: Session = Depends(get_db)):
    if not await crud.delete_faqs(ids, db):  
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", description="read faqs", response_model = List[schemas.FAQs])
async def read_faqs(search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_faqs(search, value, db)

@router.get("/{id}", description="read faqs by id",response_model = schemas.FAQs)
async def read_faq_by_id(id: int, db: Session = Depends(get_db)):
    faq = await crud.read_faq_by_id(id, db)
    if not faq:
        raise HTTPException(status_code=404)
    return faq
