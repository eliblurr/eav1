from fastapi.staticfiles import StaticFiles
from main import api
import os

static_DIR = os.path.dirname(os.path.relpath(__file__))

api.mount("/api/images", StaticFiles(directory="{dir}".format(dir=os.environ.get('MEDIA_URL') or static_DIR+"/images")), name="media")