from ..location_router.crud import read_location_by_id
from helper import FolderIO, ImageFolderIO
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from static.main import ad_DIR
from . import models, schemas
import sys, pydantic, utils
from sqlalchemy import exc
from typing import List

folder_io = FolderIO(ad_DIR)
image_folder_io = ImageFolderIO(ad_DIR, 15, folder_io, 'ads')

async def create_ad(payload:schemas.CreateAd, images, db: Session):
    # if not (payload.title and payload.metatitle and payload.description and images):
    #     raise HTTPException(status_code=422)

    if payload.style_id and await read_style_by_id(payload.style_id, db) is None:
        raise HTTPException(status_code=404, detail="style not found")
    
    

    payload_cp = payload.dict(exclude_unset=True).copy()
    del payload_cp['location_ids']
    print(payload_cp)

    try:
        pass
        # if len(payload.location_ids):
            # print(payload.location_ids)
        # if payload.style_id:
        
        # title=title, metatitle=metatitle, description=description, status=status, 
        # style_id=style_id, 
        # location_ids=location_ids
        
        new_ad = models.Ads(**payload_cp)
        db.add(new_ad) 
        db.flush()
        if len(payload.location_ids):
            location_ids = await utils.string_list_to_int_list(payload.location_ids[0].split(","))
            if len(location_ids):
                location = await read_location_by_id(id, db)
                if location:
                    new_ad.locations.append(location)

            # print(location_ids)
        # 
        #     urls, folder_name = await image_folder_io.create(images, 700, 500)
        #     for url in urls:
        #         url = models.AdImages(image_url=url, folder_name=folder_name)
        #         
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

async def create_style(payload, db:Session):
    if not bool(payload.dict(exclude_unset=True)):
        raise HTTPException(status_code=422)
    payload_cp = payload.dict(exclude_unset=True).copy()
    for k,v in payload_cp.items():
        if isinstance(v,pydantic.color.Color):
            pass
            payload_cp[k] = v.__str__()
    try:
        new_style = models.Styles(**payload_cp)
        db.add(new_style) 
        db.commit()
        db.refresh(new_style)
        return new_style
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_styles(skip:int, limit:int, search:str, value:str, db:Session):
    base = db.query(models.Styles)
    if search and value:
        try:
            base = base.filter(models.Styles.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_style_by_id(id:int, db:Session):
    return db.query(models.Styles).filter(models.Styles.id==id).first()

async def update_style(id:int, payload:schemas.UpdateStyle, db:Session):
    if not await read_style_by_id(id, db):
        raise HTTPException(status_code=404)
    payload_cp = payload.dict(exclude_unset=True).copy()
    for k,v in payload_cp.items():
        if isinstance(v,pydantic.color.Color):
            pass
            payload_cp[k] = v.__str__()
    try:
        updated = db.query(models.Styles).filter(models.Styles.id==id).update(payload_cp)
        db.commit()
        if bool(updated):
            return await read_style_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_style(id:int, db:Session):
    try:
        style = await read_style_by_id(id, db)
        if style:
            db.delete(style)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)