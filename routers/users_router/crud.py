from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from fastapi import Depends, HTTPException
from ..auth_router.models import AuthType
from sqlalchemy.orm import Session
from . import models, schemas
from main import get_db
import sqlalchemy
import utils
import sys

async def create_user(payload: schemas.UserCreate , db: Session = Depends(get_db)):

    auth_type = db.query(AuthType).filter(AuthType.id == payload.auth_type_id).first()
    if not auth_type:
        raise HTTPException(status_code=404, detail="could not find auth_type that corresponds to the user you are trying to create" )
    
    info = {k:v for (k,v) in payload.dict().items() if k != 'email' and k != 'password' and k != 'auth_type_id'}

    try:  
        new_user = models.User(email=payload.email, password=models.User.generate_hash(payload.password),auth_type=auth_type)
        db.add(new_user)

        user_info = models.UserInfo(**info,user=new_user)
        db.add(user_info) 

        db.commit()
        db.refresh(new_user) 

        return new_user

    except IntegrityError:
        db.rollback()
        #log error here
        raise HTTPException(status_code=409, detail="user with email {} already exists".format(payload.email))
    except:
        db.rollback()
        #log error here
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None ):
    try:
        base = db.query(models.User)
        if search and value:
            try:
                base = base.filter(models.User.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        #log error here
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )
        
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == id).first()

async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).first()
    
async def delete_user(id: int, db):
    try:
        user = await get_user_by_id(id, db)
        if user:
            db.delete(user)
            db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def update_user(id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):

    if not await get_user_by_id(id, db):
        raise HTTPException(status_code=404, detail="user not found")

    try:

        res = db.query(models.UserInfo).filter(models.UserInfo.user_id == id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        return await get_user_by_id(id, db)

    except IntegrityError:
        db.rollback()
        # log error here
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")

    except:
        db.rollback()
        # log error here
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def verify_password(id, payload: schemas.ResetPassword, db: Session):
    user = await get_user_by_id(id,db)
    if not user:
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    return models.User.verify_hash(payload.password, user.password)

async def reset_password(id, payload: schemas.ResetPassword, db: Session):

    if not await get_user_by_id(id,db):
        raise HTTPException(status_code=404, detail="user with id: {} was not found".format(id))
    
    try:
        res = db.query(models.User).filter(models.User.id == id).update({'password':models.User.generate_hash(payload.password)})
        db.commit()
        return await get_user_by_id(id, db)
    
    except:
        db.rollback()
        # log error here
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))