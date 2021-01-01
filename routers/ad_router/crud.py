from ..location_router.crud import read_location_by_id
from helper import FolderIO, ImageFolderIO
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from static.main import ad_DIR
from . import models, schemas
from sqlalchemy import exc
from typing import List
import sys

folder_io = FolderIO(ad_DIR)
image_folder_io = ImageFolderIO(ad_DIR, 15, folder_io, 'ads')

async def create_ad(payload:schemas.CreateAd, images, db: Session):
    try:
        new_ad = models.Ads(**payload.dict())
        db.add(new_ad) 
        db.flush()
        if len(images):
            urls, folder_name = await image_folder_io.create(images, 700, 500)
            for url in urls:
                url = models.AdImages(image_url=url, folder_name=folder_name)
                new_ad.images.append(url)
        db.commit()
        db.refresh(new_ad)
        return new_ad
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_ads(skip:int, limit:int, search:str, value:str, location_id:int, db:Session):
    base = db.query(models.Ads)
    if location_id:
        location = await read_location_by_id(location_id, db)
        if location is not None:
            base = location.location_ads
    if search and value:
        try:
            base = base.filter(models.Ads.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_ad_by_id(id:int, db:Session):
    return db.query(models.Ads).filter(models.Ads.id == id).first()

async def update_ad(id:int, payload:schemas.UpdateAd, db:Session):
    if not await read_ad_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Ads).filter(models.Ads.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_ad_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_ad(id:int, db:Session):
    try:
        ad = await read_ad_by_id(id, db)
        if ad:
            if len(ad.images):
                await utils.delete_folder(ad_DIR+"/"+ad.images[0].folder_name)
            db.delete(ad)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_image_ad(id:int, images, db:Session):
    ad = await read_ad_by_id(id, db)
    if not ad:
        raise HTTPException(status_code=404)
    try:
        urls, folder_name = await image_folder_io.append_image(ad, images, 700, 500)
        if urls and folder_name:
            for url in urls:
                url = models.AdImages(image_url=url, folder_name=folder_name)
                ad.images.append(url)
        db.commit()
        db.refresh(ad)
        return ad
    except:      
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_image_ad(id:int, db:Session):
    ad_image = db.query(models.AdImages).filter(models.AdImages.id == id).first()
    try: 
        if ad_image:
            _ , folder_name, image_name = ad_image.image_url.split("/")
            if await utils.file_exists(ad_DIR+"/"+folder_name+"/"+image_name) and await utils.delete_file(ad_DIR+"/"+folder_name+"/"+image_name):
                db.delete(ad_image)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)