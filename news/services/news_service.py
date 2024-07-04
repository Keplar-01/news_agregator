from datetime import datetime, timedelta
from typing import Type, List, Optional

import pandas as pd
from sqlalchemy.orm import Session

from repositories.news_repository import NewsRepository
from schemas import news_schema as _schema_news
from repositories.classes_repository import ClassesRepository


class NewsService():
    def __init__(self, session: Session):
        self.news_repository = NewsRepository(session)
        self.classes_repository = ClassesRepository(session)

    async def create(self, news: _schema_news.NewsInput) -> _schema_news.NewsOutput:
        return await self.news_repository.create(news)

    async def get_all(self, date_from: Optional[datetime] = None,
                      date_to: Optional[datetime] = None,
                      classes: Optional[List[int]] = None,
                      limit: int | None = None,
                      offset: int | None = None,
                      is_train: bool = False,
                      is_positive: bool = None
                      ) -> List[Type[_schema_news.NewsOutput]]:
        news = await self.news_repository.get_all(date_from=date_from, date_to=date_to, classes=classes, limit=limit,
                                                  offset=offset, is_train=is_train, is_positive=is_positive)

        classes = await self.classes_repository.get_all()
        classes = {c.id: c.description for c in classes if c.is_active}
        result = []

        for n in news:
            if n.classes_id is None:
                continue
            n.classes_names = "".join(description for id, description in classes.items() if id == n.classes_id)

            result.append(n)

        return result

    async def get_news_by_user(self, user_id: int, date_from: Optional[datetime] = None,
                               date_to: Optional[datetime] = None, classes: Optional[List[int]] = None, limit=25,
                               offset=0) -> List[Type[_schema_news.NewsOutput]]:
        news = await self.news_repository.get_user_news(user_id, date_from=date_from, date_to=date_to, classes=classes,
                                                        limit=limit, offset=offset)
        classes = await self.classes_repository.get_all()
        classes = {c.id: c.name for c in classes if c.is_active}
        result = []
        for n in news:
            if n.classes_id is None:
                continue
            n.classes_names = "".join(c.name for c in classes if c.id == n.classes_id)
            result.append(n)
        return result

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
            return {"success": False, "result": "Запись не найдена"}

        is_valid = await self.news_repository.get_by_url(data.url)

        if is_valid is not None and is_valid.id != news_id:
            return {"success": False, "result": "Запись с таким url уже существует"}

        db_news_data = await self.news_repository.update(db_news_data, data)

        return {"success": True, "result": _schema_news.NewsOutput.from_orm(db_news_data)}

    async def delete(self, news_id):
        news = await self.news_repository.get_by_id(news_id)
        if not news:
            return False
        return await self.news_repository.delete(news)

    async def get_news_to_check(
            self,
            date_to: Optional[datetime] = datetime.now() - timedelta(days=2),
            classes_ids: Optional[List[int]] = None
    ) -> Type[_schema_news.NewsOutput]:
        classes = await self.classes_repository.get_all()
        classes = {c.id: c.description for c in classes if c.is_active}
        print(date_to)
        news = await self.news_repository.get_all(date_to=date_to)
        for n in news:
            if n.text == "" or (len(classes_ids) > 0 and n.classes_id in classes_ids):
                continue
            n.classes_names = "".join(description for id, description in classes.items() if id == n.classes_id)
            return n

    async def update_train_classes(self, classes_id: int, news_id: int) -> Type[_schema_news.NewsOutput]:
        news = await self.news_repository.get_by_id(news_id)
        news.classes_id = classes_id
        news.is_train = True
        news_dict = {k: v for k, v in news.__dict__.items() if not k.startswith('_')}
        update_data = _schema_news.NewsInput(**news_dict)

        return await self.news_repository.update(news, update_data)

    async def get_train_news(self):
        news = await self.news_repository.get_all(is_train=True)

        classes = await self.classes_repository.get_all()
        classes_dict = {c.id: c.description for c in classes}

        df = pd.DataFrame([(classes_dict.get(n.classes_id, "Unknown"), n.text) for n in news],
                          columns=['class', 'text'])

        df.to_csv('train_news.csv', index=False)

        return 'train_news.csv'

    async def get_count_by_сlasses(self, classes: List[int] = None) -> dict:
        news = await self.news_repository.get_news_count_by_class(classes)
        return {class_id: count for class_id, count in news}