import os
import sys

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from config.database import Session
from services.ml_model_service import MlModelService
from routes import ml_router
from services.disk_service import DiskService
from services.producer_service import Producer, producer, producer_contol
from services.consumer_service import start_consumer
from routes import parser_route, news_route, auth, user_route
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs import schedule as _schedule
sys.path.append(os.path.dirname(__file__))
app = FastAPI()
_service_ml = MlModelService(Session())
origins = [
    "http://localhost:3000",
]
http_bearer = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print('Запуск сервера')
    _schedule.scheduler.start()
    start_consumer()
    await producer.connect()
    await producer_contol.connect()
    _service_disk = DiskService()
    await _service_ml.set_active_model()

@app.on_event("shutdown")
async def shutdown():
    print('Остановка сервера')
    _schedule.scheduler.shutdown()

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(parser_route.router)
router.include_router(news_route.router)
router.include_router(auth.router)
router.include_router(user_route.router)
router.include_router(ml_router.router)
app.include_router(router)