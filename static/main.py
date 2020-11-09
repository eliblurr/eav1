from main import api

from fastapi.staticfiles import StaticFiles

import os

static_DIR = os.path.dirname(os.path.relpath(__file__))

api.mount("/api/static", StaticFiles(directory="{static_DIR}".format(static_DIR=static_DIR)), name="media")



