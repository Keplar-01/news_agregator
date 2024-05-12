import os
import sys

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from services.ml_model_service import MlModelService
from routes import parser_route, news_route
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs import schedule as _schedule
sys.path.append(os.path.dirname(__file__))

app = FastAPI()

origins = [
    "http://localhost:3000",  # React app
]

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

@app.on_event("shutdown")
async def shutdown():
    print('Остановка сервера')
    _schedule.scheduler.shutdown()

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(parser_route.router)
router.include_router(news_route.router)
app.include_router(router)