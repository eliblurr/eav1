from ..users_router.crud import get_user_by_email, get_user_by_id
from fastapi import Depends, HTTPException, BackgroundTasks
from services.email import send_in_background
from datetime import datetime, timedelta
from ..users_router.models import User
from sqlalchemy.orm import Session
from main import get_db, scheduler
from . import models, schemas
from sqlalchemy import or_
import sqlalchemy
import utils
import sys
import os

from database import SessionLocal

access_token_duration = timedelta(minutes= os.environ.get('ACCESS_TOKEN_DURATION_IN_MINUTES') or 30)
refresh_token_duration = timedelta(days= os.environ.get('REFRESH_TOKEN_DURATION_IN_MINUTES') or 87000)
reset_password_session_duration = os.environ.get('RESET_PASSWORD_SESSION_DURATION_IN_MINUTES') or 1

async def authenticate(payload: schemas.Auth, db: Session):
    user = await get_user_by_email(payload.email, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    if User.verify_hash(payload.password, user.password):
        access_token = utils.create_access_token(data = {'email':payload.email,'id':user.id}, expires_delta=access_token_duration)
        refresh_token = utils.create_refresh_token(data = {'email':payload.email,'id':user.id}, expires_delta=refresh_token_duration)

        return {
            "access_token": access_token.decode("utf-8"),
            "refresh_token": refresh_token.decode("utf-8"),
            'user': user
        }

    else:
        raise HTTPException(status_code=401, detail="authentication failed")

async def revoke_token(payload: schemas.Token, db: Session):
    try:
        if payload.access_token:
            revoke_access_token = models.RevokedToken(jti=payload.access_token)
            db.add(revoke_access_token)
        
        if payload.refresh_token:
            revoke_refresh_token = models.RevokedToken(jti=payload.refresh_token)
            db.add(revoke_refresh_token)
        
        db.commit()
        db.close()
        return True
       
    except:
        db.rollback()
        db.close()
        raise HTTPException(status_code=401, detail="authentication failed")

async def refresh_token(payload: schemas.Token, db: Session):
    data = utils.decode_token(data=payload.refresh_token)

    if not await revoke_token(payload, db):
        raise HTTPException(status_code=417,detail="failed to revoke access token")

    access_token = utils.create_access_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=access_token_duration)
    refresh_token = utils.create_refresh_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=refresh_token_duration)

    return {
        'access_token': access_token.decode("utf-8"),
        'refresh_token': refresh_token.decode("utf-8"),
    }

async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti == token).first()
    db.close()
    if res is None:
        return False
    return True

async def request_password_reset(payload: schemas.Email, db: Session, background_tasks: BackgroundTasks):
    user = await get_user_by_email(payload.email, db)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    while True:
        new_code = models.ResetPasswordCodes(user_id = user.id, code = models.ResetPasswordCodes.generate_code())

        code = db.query(models.ResetPasswordCodes).filter(or_(
            models.ResetPasswordCodes.user_id == user.id,
            models.ResetPasswordCodes.code == new_code.code
        )).first()

        if code:
            try:
                db.delete(code)
                db.commit()
                break
            except:
                raise HTTPException(status_code=500)
        else:
            break
    
    try:
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        scheduler.add_job(delete_password_reset_code, trigger='date', kwargs={'id': new_code.id}, id='ID{}'.format(new_code.id), replace_existing=True, run_date=datetime.utcnow()+timedelta(minutes=reset_password_session_duration))
        await send_in_background(background_tasks, ['{}'.format(payload.email)], new_code.code)
        return new_code
    except:
        db.rollback()
        db.close()

def delete_password_reset_code(id: int, db: Session = SessionLocal()):
    try:
        code = db.query(models.ResetPasswordCodes).filter(models.ResetPasswordCodes.id == id).first()
        if code:
            db.delete(code)
            db.commit()
        return True
    except:
        raise HTTPException(status_code=500)