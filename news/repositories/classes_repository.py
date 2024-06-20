from typing import Type

from config.database import Session
from repositories.interface_repository import RepositoryInterface
from models import classes as _orm
from schemas import classes_schema as _schema

class ClassesRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    async def get_all(self) -> list[Type[_orm.Classes]]:
        return self.session.query(_orm.Classes).all()

    async def get_by_id(self, classes_id: int) -> _orm.Classes:
        return self.session.query(_orm.Classes).filter(_orm.Classes.id == classes_id).first()

    async def get_by_name(self, name: str) -> _orm.Classes:
        return self.session.query(_orm.Classes).filter(_orm.Classes.name == name).first()

    async def update(self, classes: _orm.Classes, data: _schema.ClassesInput) -> _orm.Classes:
        old_value_fields = classes.__dict__

        for field in old_value_fields:
            if field in data and field != '_sa_instance_state':
                setattr(classes, field, data[field])

        self.session.commit()
        self.session.refresh(classes)

        return classes

    async def delete(self, item: _orm.Classes) -> bool:
        self.session.delete(item)
        self.session.commit()
        return True

    async def create(self, item: _schema.ClassesInput) -> _orm.Classes:
        db_classes = _orm.Classes(**item.dict())
        self.session.add(db_classes)
        self.session.commit()
        self.session.refresh(db_classes)
        return db_classes