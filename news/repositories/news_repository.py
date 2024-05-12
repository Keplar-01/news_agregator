from datetime import datetime
from typing import Type, List, Optional

from sqlalchemy.orm import Session

from models import news as _orm
from schemas import news_schema as _schema

class NewsRepository():
    def __init__(self, session: Session):
        self.session = session

    async def get_all(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, classes: Optional[List[str]] = None) -> list[
        Type[_orm.News]]:
        query = self.session.query(_orm.News)

        if date_to is not None:
            query = query.filter(_orm.News.date <= date_to)

        if date_from is not None:
            query = query.filter(_orm.News.date >= date_from)

        if classes is not None:
            query = query.filter(_orm.News.classes.in_(classes))

        return query.all()

    async def get_by_id(self, news_id: int) -> _orm.News:
        return self.session.query(_orm.News).filter(_orm.News.id == news_id).first()

    async def get_by_url(self, url: str) -> _orm.News:
        return self.session.query(_orm.News).filter(_orm.News.url == url).first()

    async def get_by_classes(self, classes: str) -> List[Type[_orm.News]]:
        return self.session.query(_orm.News).filter(_orm.News.classes == classes).all()

    async def get_by_classes_list(self, classes: List[str]) -> List[Type[_orm.News]]:
        return self.session.query(_orm.News).filter(_orm.News.classes.in_(classes)).all()

    async def update(self, news: _orm.News, data: _schema.NewsInput) -> _orm.News:
        old_value_fields = news.__dict__

        for field in old_value_fields:
            if field in data.dict() and field != '_sa_instance_state':
                setattr(news, field, data.dict()[field])

        self.session.commit()
        self.session.refresh(news)

        return news

    async def delete(self, news: _orm.News) -> bool:
        self.session.delete(news)
        self.session.commit()
        return True

    async def create(self, news: _orm.News) -> _orm.News:
        new_record = _orm.News(**news.dict())
        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
        return new_record