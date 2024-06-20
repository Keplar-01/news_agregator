import asyncio
import os
from datetime import datetime, timedelta
from typing import List, Annotated, Union, Optional, Dict

from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Query

from config.database import Session
from keras.src.saving import load_model
from schemas import news_schema as _schema_news
from schemas import classes_schema as _schema_classes
from services.news_service import NewsService
from services.auth_service import AuthService, _auth_cur_user_access
from services.producer_service import producer
from services.classes_service import ClassesService
from schemas.user_schema import UserOutput


_service = NewsService(Session())

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 # Замените 'task_queue' на имя вашей очереди

router = APIRouter(
    prefix="/news",
    tags=["news"]
)
auth_service = AuthService(Session())
classes_service = ClassesService(Session())
from services.auth_service import oauth2_scheme


@router.get("",
            response_model=List[_schema_news.NewsOutput])
async def get_news(date_from: Optional[datetime] = None,
                   date_to: Optional[datetime] = None,
                   classes: Optional[str] = None,
                   is_positive: Optional[bool] = None,
                   limit: Optional[int] = None,
                   offset: Optional[int] = None,
                   ) -> List[_schema_news.NewsOutput]:
    classes = classes.split(',') if classes else None
    data = await _service.get_all(
        date_from=date_from,
        date_to=date_to,
        classes=classes,
        limit=limit,
        offset=offset,
        is_train=False,
        is_positive=is_positive
    )
    return data

@router.get("/train_one", response_model=_schema_news.NewsOutput)
async def get_news_to_check(
        date_to: Optional[datetime] = datetime.now() - timedelta(days=2),
        classes: Optional[str] = Query(None)
    ) -> List[_schema_news.NewsOutput]:
    classes_ids = [int(id) for id in classes.split(',')] if classes else None
    data = await _service.get_news_to_check(
        date_to=date_to,
        classes_ids=classes_ids
    )
    return data


@router.get("/count_by_classes", response_model=Dict[int, int])
async def get_news_count_by_classes(classes_ids: Optional[str] = None):
    classes = classes_ids.split(',') if classes_ids else None
    return await _service.get_count_by_сlasses(classes)

@router.put("/train/{news_id}", response_model=_schema_news.NewsOutput)
async def update_train_classes(news_id: int, classes_id: int):
    return await _service.update_train_classes(classes_id, news_id)

@router.get("/train_news", response_class=FileResponse)
async def get_train_news_file():
    filename = await _service.get_train_news()
    return FileResponse(filename, media_type='application/octet-stream', filename='train_news.csv')

@router.get("/user",
            dependencies=[Depends(auth_service.role_req("admin", "user"))],
            response_model=List[_schema_news.NewsOutput])
async def get_news_by_user(
        user: UserOutput = Depends(_auth_cur_user_access),
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        classes: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[_schema_news.NewsOutput]:
    classes = classes.split(',') if classes else None
    data = await _service.get_news_by_user(user.id, date_from=date_from, date_to=date_to, classes=classes, limit=limit, offset=offset)
    return data

@router.post('/add',
dependencies=[Depends(oauth2_scheme)],
             response_model=_schema_news.NewsOutput)
async def create_news(news: _schema_news.NewsInput) -> _schema_news.NewsOutput:
    return await _service.create(news)


@router.put("/update_classes",dependencies=[Depends(oauth2_scheme)])
async def get_class() -> List[str]:
    data = await _service.get_all()
    news_list = []
    for news in data:
        await producer.send({"text_id":news.id, "text":news.text, "correlation_id": str(news.id)})
    return news_list


@router.put("/update", dependencies=[Depends(oauth2_scheme)])
async def update_news(news_id: int, news: _schema_news.NewsInput) -> dict:
    return await _service.update(news_id, news)


@router.get('/classes')
async def get_classes() -> List[_schema_classes.ClassesOutput]:
    return await classes_service.get_all()


@router.post('/classes', dependencies=[Depends(oauth2_scheme)])
async def create_class(class_name: _schema_classes.ClassesInput) -> _schema_classes.ClassesOutput:
    return await classes_service.create(class_name)


@router.get("/{news_id}",
            response_model=_schema_news.NewsOutput)
async def get_news_by_id(news_id: int) -> _schema_news.NewsOutput:
    news = await _service.get_by_id(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news
