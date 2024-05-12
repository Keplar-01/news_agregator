import os
from datetime import datetime
from typing import List, Annotated, Union, Optional
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends

from config.database import Session
from keras.src.saving import load_model
from schemas import news_schema as _schema_news

from services.news_service import NewsService
from services.ml_model_service import MlModelService

_service = NewsService(Session())

_ml_service = MlModelService()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ml_service.set_model('model_svm.pkl')

router = APIRouter(
    prefix="/news",
    tags=["news"]
)


@router.get("",
            response_model=List[_schema_news.NewsOutput])
async def get_news(date_from: Optional[datetime] = None, date_to: Optional[datetime] = None,
                   classes: Optional[str] = None) -> List[_schema_news.NewsOutput]:
    classes = classes.split(',') if classes else None
    data = await _service.get_all(date_from=date_from, date_to=date_to, classes=classes)
    return data


@router.post('/add',
             response_model=_schema_news.NewsOutput)
async def create_news(news: _schema_news.NewsInput) -> _schema_news.NewsOutput:
    return await _service.create(news)

@router.get("/update_classes")
async def get_class()-> List[str]:
    data = await _service.get_all()
    news_list = []
    for news in data:
        news.classes = _ml_service.predict(_ml_service.model, news.text, 'pkl')
        news_input = _schema_news.NewsInput.from_orm(news)
        await _service.update(news.id, news_input)
        news_list.append(news.classes)
    return news_list

@router.get("/{news_id}",
            response_model=_schema_news.NewsOutput)
async def get_news_by_id(news_id: int) -> _schema_news.NewsOutput:
    news = await _service.get_by_id(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news



