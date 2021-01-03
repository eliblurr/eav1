from ..users_router.crud import read_user_by_email, read_user_by_id
from fastapi import Depends, HTTPException, BackgroundTasks
from services.email import send_in_background
from datetime import datetime, timedelta
from ..users_router.models import User
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import or_, exc
from . import models, schemas
from main import scheduler
import utils, sys, os

access_token_duration = timedelta(minutes= os.environ.get('ACCESS_TOKEN_DURATION_IN_MINUTES') or 30)
refresh_token_duration = timedelta(days= os.environ.get('REFRESH_TOKEN_DURATION_IN_MINUTES') or 87000)
reset_password_session_duration = os.environ.get('RESET_PASSWORD_SESSION_DURATION_IN_MINUTES') or 1

async def authenticate(payload: schemas.Auth, db: Session):
    user = db.query(User).filter(User.email==payload.email).first()
    if not user:
        raise HTTPException(status_code=404)
    if User.verify_hash(payload.password, user.password):
        try:
            access_token = utils.create_access_token(data = {'email':payload.email,'id':user.id}, expires_delta=access_token_duration)
            refresh_token = utils.create_refresh_token(data = {'email':payload.email,'id':user.id}, expires_delta=refresh_token_duration)
            return {"access_token": access_token.decode("utf-8"), "refresh_token": refresh_token.decode("utf-8"), "user": user}
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=401)

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
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def refresh_token(payload: schemas.Token, db: Session):
    if not payload.refresh_token: 
        raise HTTPException(status_code=422)
    if await is_token_blacklisted(payload.refresh_token, db):
        raise HTTPException(status_code=401)
    if await revoke_token(payload, db):
        try:
            data = utils.decode_token(data=payload.refresh_token)
            access_token = utils.create_access_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=access_token_duration)
            refresh_token = utils.create_refresh_token(data = {'email':data.get('email'),'id':data.get('id')}, expires_delta=refresh_token_duration)
            return {'access_token': access_token.decode("utf-8"), 'refresh_token': refresh_token.decode("utf-8")}
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=417)
    
async def is_token_blacklisted(token: str, db: Session):
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti == token).first()
    if res is None:
        return False
    return True

async def request_password_reset(payload: schemas.Email, db: Session, background_tasks: BackgroundTasks):
    user = db.query(User).filter(User.email==payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    while True:
        new_code = models.ResetPasswordCodes(user_id=user.id, code=models.ResetPasswordCodes.generate_code())
        code = db.query(models.ResetPasswordCodes).filter(models.ResetPasswordCodes.user_id==user.id).first()
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
        return True
    except:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

def delete_password_reset_code(id: int, db: Session = SessionLocal()):
    try:
        code = db.query(models.ResetPasswordCodes).filter(models.ResetPasswordCodes.id==id).first()
        if code:
            db.delete(code)
        db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)