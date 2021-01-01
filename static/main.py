from fastapi.staticfiles import StaticFiles
from main import api
import os

static_DIR = os.path.dirname(os.path.relpath(__file__))
image_DIR = "{static_DIR}/images".format(static_DIR=static_DIR)
category_DIR = "{image_DIR}/categories".format(image_DIR=image_DIR)
product_DIR = "{image_DIR}/products".format(image_DIR=image_DIR)
event_DIR = "{image_DIR}/events".format(image_DIR=image_DIR)
ad_DIR = "{image_DIR}/ads".format(image_DIR=image_DIR)

api.mount("/api/images", StaticFiles(directory="{dir}".format(dir=os.environ.get('image_DIR') or image_DIR)), name="images")