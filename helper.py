from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_
from typing import List
from io import BytesIO
from PIL import Image
import utils
import sys

class CRUD:
    def __init__(self,  model, db):
        self.db = db
        self.model = model
    
    async def read(self, search:str = None, value:str = None, skip: int=0, limit: int=100 ):
        base = self.db.query(self.model)
        if search and value:
            try:
                base = base.filter(self.model.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.all()
        return base.all()
    
    async def read_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).first()

    async def update(self, id, payload):
        if not await self.read_about_us_by_id(id, self.db):
            raise HTTPException(status_code=404)
        
        try:
            self.db.query(self.model).filter(self.model.id == id).update(payload.dict(exclude_unset=True))
            self.db.commit()
            return await self.read_about_us_by_id(id, self.db)
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=422, detail="unique constraint on index failed")

        except:
            self.db.rollback()
            print("{}".format(sys.exc_info()))  

    async def delete(self, id):
        try:
            item = await self.read_by_id(id)
            if item:
                self.db.delete(item)
                self.db.commit()
            return True
        except:
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    
    async def filter_range(self, skip: int=0, limit: int=100, search:str = None, lower_boundary: float=0, upper_boundary:float=0):
        try:
            base = self.db.query(self.model)
            if lower_boundary and upper_boundary:
                try: 
                    base = base.filter(and_(
                        self.model.__table__.c[search] <= upper_boundary,
                        self.model.__table__.c[search] >= lower_boundary
                    ))
                except KeyError:
                    return base.offset(skip).limit(limit).all()
            return base.offset(skip).limit(limit).all()
        except:
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

    async def create(self, payload):
        try:  
            item = self.model(**payload.dict())
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item) 
            return item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="" )
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )     

class FileIO:
    def __init__(self, directory):
        self.directory = directory

    async def create(self, files: List = []):
        try:
            for file in files:
                file = await file.read()
                file_id = utils.gen_alphanumeric_code_lower(length=20)
                file_type = file.content_type.split('/')
                file_directory = "{directory}/{file_id}.{file_type}".format(directory=self.directory, file_id=file_id, file_type=file_type[1])
                if await utils.create_file(file_directory, image):
                    return file_directory                
        except OSError:
            print("{}".format(sys.exc_info()))
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500, detail="something went wrong while trying to add images")

    async def delete(self, files: List = []):
        try:
            for file in files:
                file_url = "{directory}/{file}".format(directory=self.directory, file=file)
            if await utils.delete_file(file_url):
                return file_directory                
        except OSError:
            print("{}".format(sys.exc_info()))
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500, detail="something went wrong while trying to delete images")

class FolderIO:
    def __init__(self, directory):
        self.directory = directory

    async def create(self, folder_name):
        self.folder_name = folder_name
        try:
            if await utils.create_folder( "{directory}/{folder_name}".format(directory=self.directory, folder_name=folder_name) ):
                return True   
        except OSError:
            print ("Creation of the directory %s failed" % folder_name)   
            print("{}".format(sys.exc_info()))   
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500, detail="something went wrong while trying to add folder")

    async def delete(self, folder_name):
        try:
            if await utils.delete_folder( "{directory}/{folder_name}".format(directory=self.directory, folder_name=folder_name) ):
                return True
        except OSError:
            print ("Creation of the directory %s failed" % folder_name)
            print("{}".format(sys.exc_info()))
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500, detail="something went wrong while trying to delete folder")
        
    async def _directory(self):
        return "{}/{}".format(self.directory,self.folder_name)

class ImageIO:
    def __init__(self, directory):
        self.directory = directory
    
    async def create(self, image: bytes, image_name, image_ext ):
        try:
            image = Image.open(BytesIO(image))
            image.save("{dir}/{image_name}.{image_ext}".format(dir=self.directory, image_name=image_name,image_ext=image_ext))
            return True
        except:
            print("{}".format(sys.exc_info()))
            return False
    
    async def create_thumbnail(self, image: bytes, image_name, image_ext , x=300, y=300):
        try:
            image = Image.open(BytesIO(image))
            image.thumbnail((x,y))
            image.save("{dir}/{image_name}.{image_ext}".format(dir=self.directory, image_name=image_name,image_ext=image_ext))
            return True
        except:
            print("{}".format(sys.exc_info()))
            return False

    
    async def delete(self, url):
        try:
            if utils.delete_folder( "{directory}{url}".format(directory=self.directory, url=url) ):
                return True
        except OSError:
            print ("Creation of the directory %s failed" % folder_name)
            print("{}".format(sys.exc_info()))
        except:
            print("{}".format(sys.exc_info()))
            raise HTTPException(status_code=500, detail="something went wrong while trying to delete folder")

    async def show(self, image: bytes):
        image = Image.open(BytesIO(image))
        return image.show()

    async def resize(self, image: bytes, x, y):
        image = Image.open(BytesIO(image))
        return image.thumbnail((x, y))
    
    async def _directory(self):
        return "{}".format(self.directory)

class ImageFolderIO:
    def __init__(self, directory, length, folder_io, parent_folder):
        self.directory = directory
        self.length = length #'''folder name length'''
        self.folder_io = folder_io
        self.parent_folder = parent_folder #'''folder name for immediate parent working dir'''
    
    async def create(self, images, x, y):
        try:
            folder_name = utils.gen_alphanumeric_code_lower(length=self.length)
            while await utils.folder_exists(self.directory+"/"+folder_name):
                continue 
            if not await self.folder_io.create(folder_name):
                raise HTTPException(status_code=500, detail="failed to create dir")
            urls = []
            image_io = ImageIO(await self.folder_io._directory())
            for image in images:
                ftype, fext = image.content_type.split('/')
                fn = "img_"+str(images.index(image)+1)
                image_b = await image.read()
                if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , x, y):
                    urls.append("{parent_folder}/{folder_name}/{fn}.{fext}".format(parent_folder= self.parent_folder, folder_name=folder_name, fn=fn, fext=fext) )
                
            if not len(urls):
                await utils.delete_folder(self.directory+"/"+folder_name)    

            return urls, folder_name
        except:
            print("{}".format(sys.exc_info()))                    
            raise HTTPException(status_code=500)
    
    async def append_image_to_class(self):
        return
    
    

    # 
    #     while await utils.folder_exists(product_DIR+"/"+folder_name):
    #         continue      

    #     if not await folder_io.create(folder_name):
    #         raise HTTPException(status_code=500, detail="failed to create dir")

    #     urls = []
    #     image_io = ImageIO(await folder_io._directory())
    #     for image in images:
    #         ftype, fext = image.content_type.split('/')
    #         fn = "img_"+str(images.index(image)+1)
    #         image_b = await image.read()
    #         if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 480, 704):
    #             urls.append("products/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext) )

    # urls = []
    # try:
    #     if len(category.images) and await utils.folder_exists(category_DIR+"/"+category.images[0].folder_name):
    #         new_index = len(os.listdir(category_DIR+"/"+category.images[0].folder_name))            
    #         image_io = ImageIO(category_DIR+"/"+category.images[0].folder_name)
    #         for image in images:
    #             ftype, fext = image.content_type.split('/')
    #             fn = "img_"+str(new_index+images.index(image)+1)
    #             image_b = await image.read()
    #             if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(category_DIR+"/"+category.images[0].folder_name+"/"+fn+"."+fext):
    #                 new_image_obj = models.CategoryImages(image_url="categories/{folder_name}/{fn}.{fext}".format(folder_name=category.images[0].folder_name, fn=fn, fext=fext), folder_name=category.images[0].folder_name)
    #                 category.images.append(new_image_obj)         
    #     else: 
    #         folder_name = utils.gen_alphanumeric_code_lower(length=15)
    #         while await utils.folder_exists(category_DIR+"/"+folder_name):
    #             continue
    #         if not await folder_io.create(folder_name):
    #             raise HTTPException(status_code=500, detail="could not create dir for image store")
    #         image_io = ImageIO(await folder_io._directory())
    #         for image in images:
    #             ftype, fext = image.content_type.split('/')
    #             fn = "img_"+str(images.index(image)+1)
    #             image_b = await image.read()                
    #             if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(category_DIR+"/"+folder_name+"/"+fn+"."+fext):
    #                 new_image_obj = models.CategoryImages(image_url="categories/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext), folder_name=folder_name)
    #                 category.images.append(new_image_obj)    

