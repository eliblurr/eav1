from fastapi import APIRouter, Depends, HTTPException, status, Response
from . import crud, schemas, models
from sqlalchemy.orm import Session
from main import get_db
from typing import List

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new faqs", response_model = schemas.FAQs)
async def create_faqs(payload: schemas.CreateFAQs, db: Session = Depends(get_db)):
    return await crud.create_faqs(payload, db)

@router.patch("/{id}", description="update faqs by id", response_model = schemas.FAQs)
async def update_faqs(id:int, payload: schemas.UpdateFAQs, db: Session = Depends(get_db)):
    return await crud.update_faq(id, payload, db)

@router.delete("/", description="delete faqs", status_code = status.HTTP_202_ACCEPTED)
async def delete_faqs(ids: List[int], db: Session = Depends(get_db)):
    return await crud.delete_faqs(ids, db) 

@router.get("/", description="read faqs", response_model = List[schemas.FAQs])
async def read_faqs(skip:int=0, limit:int=100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_faqs(skip, limit, search, value, db)

@router.get("/{id}", description="read faqs by id",response_model = schemas.FAQs)
async def read_faq_by_id(id: int, db: Session = Depends(get_db)):
    faq = await crud.read_faq_by_id(id, db)
    if not faq:
        raise HTTPException(status_code=404)
    return faq
