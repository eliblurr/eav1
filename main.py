from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine

from routers.auth_router import models
from routers.category_router import models
from routers.events_router import models
from routers.priorities_router import models
from routers.t_c_router import models
from routers.location_router import models
from routers.reviews_router import models
from routers.policies_router import models
from routers.faqs_router import models
from routers.about_us_router import models 
from routers.announcement_router import models
from routers.subscriptions_router import models

import os

ROOT_DIR = os.path.dirname(os.path.relpath(__file__))

from fastapi.security import OAuth2PasswordBearer

api = FastAPI(docs_url="/api/docs")

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# job schedulars
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pytz

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///./sql_app.db')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc, misfire_grace_time=1)


# scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id')
# scheduler.remove_job('my_job_id')
# scheduler.shutdown()
# scheduler.shutdown(wait=False)
# scheduler.resume()
# scheduler.start(paused=True)
# scheduler.reschedule_job('my_job_id', trigger='cron', minute='*/5')
# triggers = date, cron, interval
# scheduler.get_jobs()
# scheduler.print_jobs()
# scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id',replace_existing=True)
# current_app.scheduler.add_job(
#         test_job, 'cron', hour=hour, minute=minute,
#         args=[name], id=job_id)
def scheduled_job():
    print('Welcome to Neutrons link')

scheduler.add_job(scheduled_job, trigger='interval', seconds=5, id='scheduled_job',replace_existing=True)


models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/authenticate")

from routers.auth_router import main as auth
from routers.product_router import main as product
from routers.promo_router import main as promo
from routers.boards_router import main as boards
from routers.favorites_router import main as favorites
from routers.category_router import main as category
from routers.order_router import main as order
from routers.events_router import main as events
from routers.priorities_router import main as priorities
from routers.location_router import main as location
from routers.policies_router import main as policies
from routers.faqs_router import main as faqs
from routers.about_us_router import main as about_us
from routers.announcement_router import main as announcement
from routers.subscriptions_router import main as subscriptions

from routers.t_c_router import main as t_c
from routers.reviews_router import main as reviews
# from media import main as media




api.include_router(auth.router,prefix="/api/users",tags=["user"])
api.include_router(product.router,prefix="/api/products",tags=["product"])
# api.include_router(promo.router,prefix="/api/promos",tags=["promo_vouchers"])
# api.include_router(boards.router,prefix="/api/boards",tags=["boards"])
# api.include_router(favorites.router,prefix="/api/favorites",tags=["user favorites"])
# api.include_router(category.router,prefix="/api/categories",tags=["category"])
# api.include_router(order.router,prefix="/api/orders",tags=["user order"])
# api.include_router(events.router,prefix="/api/events",tags=["events"])
# api.include_router(priorities.router,prefix="/api/priorities",tags=["priorities"])
# api.include_router(t_c.router,prefix="/api/t_c",tags=["terms and conditions"])
# api.include_router(location.router,prefix="/api/locations",tags=["location"])
api.include_router(reviews.router,prefix="/api/reviews",tags=["reviews"])
# api.include_router(policies.router,prefix="/api/policies",tags=["policies"])
# api.include_router(faqs.router,prefix="/api/faqs",tags=["faqs"])
# api.include_router(about_us.router,prefix="/api/about_us",tags=["about_us"])
# api.include_router(announcement.router,prefix="/api/announcements",tags=["announcements"])
# api.include_router(subscriptions.router,prefix="/api/subscriptions",tags=["subscriptions"])

# api.include_router(media.router,prefix="/api/media",tags=["media data"])






@api.get("/")
def welcome():
    return "Welcome to Neutrons link"

@api.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

@api.on_event("startup")
async def startup_event():
    print('server is active')
    scheduler.start()