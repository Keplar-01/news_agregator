from typing import Type

from sqlalchemy.orm import Session

from models import parse_data as _orm
from schemas import parse_data_schema as _schema
from repositories.interface_repository import RepositoryInterface

class ParseDataRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    async def create(self, parse_data: _schema.ParseDataInput) -> _orm.ParseData:
        db_parse_data = _orm.ParseData(**parse_data.dict())
        self.session.add(db_parse_data)
        self.session.commit()
        self.session.refresh(db_parse_data)
        return db_parse_data

    async def get_all(self) -> list[_orm.ParseData]:
        return self.session.query(_orm.ParseData).all()

    async def get_by_id(self, parse_data_id: int) -> _orm.ParseData:
        return self.session.query(_orm.ParseData).filter(_orm.ParseData.id == parse_data_id).first()

    async def get_by_url_list(self, url_list: str) -> _orm.ParseData:
        return self.session.query(_orm.ParseData).filter(_orm.ParseData.url_list == url_list).first()

    async def update(self, parse_data: _orm.ParseData, data: _schema.ParseDataInput) -> _orm.ParseData:
        old_value_fields = parse_data.__dict__

        for field in old_value_fields:
            if field in data.dict() and field != '_sa_instance_state':
                setattr(parse_data, field, data.dict()[field])

        self.session.commit()
        self.session.refresh(parse_data)

        return parse_data

    async def delete(self, parse_data: _orm.ParseData) -> bool:
        self.session.delete(parse_data)
        self.session.commit()
        return True