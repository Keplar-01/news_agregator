from datetime import datetime
from typing import Type, List, Optional

from sqlalchemy.orm import Session

from repositories.news_repository import NewsRepository
from schemas import news_schema as _schema_news

class NewsService():
    def __init__(self, session: Session):
        self.news_repository = NewsRepository(session)

    async def create(self, news: _schema_news.NewsInput) -> _schema_news.NewsOutput:
        return await self.news_repository.create(news)

    async def get_all(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, classes: Optional[List[str]] = None) -> List[Type[_schema_news.NewsOutput]]:
        return await self.news_repository.get_all(date_from=date_from, date_to=date_to, classes=classes)

    async def get_by_id(self, news_id: int) -> _schema_news.NewsOutput:
        return await self.news_repository.get_by_id(news_id)

    async def get_by_url(self, url: str) -> _schema_news.NewsOutput:
        return await self.news_repository.get_by_url(url)

    async def get_by_classes(self, classes: str) -> List[Type[_schema_news.NewsOutput]]:
        return await self.news_repository.get_by_classes(classes)

    async def get_by_classes_list(self, classes: List[str]) -> List[Type[_schema_news.NewsOutput]]:
        return await self.news_repository.get_by_classes_list(classes)

    async def update(self, news_id: int, data: _schema_news.NewsInput) -> dict:
        db_news_data = await self.news_repository.get_by_id(news_id)

        if not db_news_data:
            return {"success": False, "result":  "Запись не найдена"}

        is_valid = await self.news_repository.get_by_url(data.url)

        if is_valid is not None and is_valid.id != news_id:
            return {"success": False, "result": "Запись с таким url уже существует"}

        db_news_data = await self.news_repository.update(db_news_data, data)

        return {"success": True, "result":  _schema_news.NewsOutput.from_orm(db_news_data)}

    async def delete(self, news_id):
        news = await self.news_repository.get_by_id(news_id)
        if not news:
            return False
        return await self.news_repository.delete(news)
