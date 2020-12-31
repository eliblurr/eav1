from ..auth_router.models import AuthType, ResetPasswordCodes
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc, and_
from . import models, schemas
from typing import List
import sys

async def create_user(payload: schemas.CreateUser , db: Session):
    auth_type = db.query(AuthType).filter(AuthType.id == payload.auth_type_id).first()
    user_type = db.query(models.UserType).filter(models.UserType.id == payload.user_type_id).first()
    res = (auth_type is not None, user_type is not None)
    if all(res):
        pass
    else:
        raise HTTPException(status_code=404, detail="{} not found".format('auth_type' if not(res[0]) else 'user_type'))
    info = {k:v for (k,v) in payload.dict().items() if k != 'email' and k != 'password' and k != 'auth_type_id' and k != 'user_type_id'}
    try:  
        new_user = models.User(email=payload.email, password=models.User.generate_hash(payload.password), auth_type_id=payload.auth_type_id, user_type_id=payload.user_type_id)
        db.add(new_user)
        db.flush()
        db.add(models.UserInfo(**info,user=new_user)) 
        db.commit()
        db.refresh(new_user) 
        return new_user
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_users(skip:int, limit:int, search:str, value:str, db: Session):
    try:
        base = db.query(models.User)
        if search and value:
            try:
                base = base.filter(models.User.email.like("%" + value + "%")) if search=='email' else base.join(models.UserInfo).filter(models.UserInfo.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()  
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
        
async def read_user_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

async def read_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email.like("%" + email + "%")).all()
    
async def delete_user(ids: List[int], db: Session):
    try:
        for id in ids:
            user = await read_user_by_id(id, db)
            if user:
                db.delete(user)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def update_user(id:int, payload:schemas.UpdateUser, db:Session):
    if not await read_user_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.UserInfo).filter(models.UserInfo.user_id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_user_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def verify_password(id, payload: schemas.ResetPassword, db: Session):
    user = await read_user_by_id(id,db)
    if not user:
        raise HTTPException(status_code=404)
    return models.User.verify_hash(payload.password, user.password)

async def reset_password(id, payload: schemas.ResetPassword, db: Session):
    if not await read_user_by_id(id, db):
        raise HTTPException(status_code=404)
    if not await verify_code(id, payload.code, db):
        raise HTTPException(status_code=417)
    try:
        updated = db.query(models.User).filter(models.User.id == id).update({'password':models.User.generate_hash(payload.password)})
        db.commit()
        if bool(updated):
            return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def verify_code(user_id, code, db: Session):
    return db.query(ResetPasswordCodes).filter(and_(ResetPasswordCodes.user_id == user_id, ResetPasswordCodes.code == code)).first()