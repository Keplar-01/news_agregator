from datetime import datetime
from typing import Type, List, Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from models import news as _orm
from schemas import news_schema as _schema

from repositories.interface_repository import RepositoryInterface

from models.user import User

from models.classes import Classes


class NewsRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    from sqlalchemy import desc

    async def get_all(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None,
                      classes: Optional[List[str]] = None, offset: Optional[int] = None,
                      limit: Optional[int] = None, is_train: bool = False, is_positive: bool = None) -> list[Type[_orm.News]]:
        query = self.session.query(_orm.News).filter(_orm.News.is_train == is_train)

        if is_positive is not None and is_positive:
            query = query.filter(_orm.News.mood == 'positive')

        if date_to is not None:
            query = query.filter(_orm.News.date <= date_to)

        if date_from is not None:
            query = query.filter(_orm.News.date >= date_from)

        if classes is not None:
            classes = list(map(int, classes))
            query = query.join(_orm.News.classes).filter(Classes.id.in_(classes))

        query = query.order_by(desc(_orm.News.date))

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

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

    async def get_user_news(self, user_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None,
                  classes: Optional[List[str]] = None, offset: Optional[int] = None,
                  limit: Optional[int] = None) -> list[
        Type[_orm.News]]:

        user = self.session.query(User).get(user_id)
        if not user:
            return []

        user_classes = [c.id for c in user.classes]
        user_parse_data = [pd.id for pd in user.parse_data]

        query = self.session.query(_orm.News).filter(
            _orm.News.classes_id.in_(user_classes),
            _orm.News.parse_data_id.in_(user_parse_data)
        )

        if date_to is not None:
            query = query.filter(_orm.News.date <= date_to)

        if date_from is not None:
            query = query.filter(_orm.News.date >= date_from)

        if classes is not None:
            classes = list(map(int, classes))
            query = query.join(_orm.News.classes).filter(Classes.id.in_(classes))

        query = query.order_by(desc(_orm.News.date))

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        return query.all()

    async def get_news_count_by_class(self, classes: list[int] = None) -> list:
        query = self.session.query(
            _orm.News.classes_id,
            func.count(_orm.News.id)
        ).group_by(
            _orm.News.classes_id
        )

        if classes is not None:
            query = query.filter(_orm.News.classes_id.in_(classes))

        return query.all()


