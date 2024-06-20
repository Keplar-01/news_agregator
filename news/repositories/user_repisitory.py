

from sqlalchemy.orm import Session
from models import user as _orm
from models import classes as _orm_classes
from models import parse_data as _orm_parse_data
from repositories.interface_repository import RepositoryInterface
from schemas import user_schema as _schema

class UserRepository(RepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    async def get_all(self):
        return self.session.query(_orm.User).all()

    async def get_by_id(self, id: int):
        return self.session.query(_orm.User).filter(_orm.User.id == id).first()

    async def get_user(self, data: dict):
        try:
            return self.session.query(_orm.User).filter_by(**data).first()
        except Exception as e:
            return None

    async def get_by_email(self, email: str):
        return self.session.query(_orm.User).filter(_orm.User.email == email).first()

    async def update(self, user, data):
        old_value_fields = user.__dict__

        for field in old_value_fields:
            if field in data.dict() and field != '_sa_instance_state':
                setattr(user, field, data.dict()[field])

        self.session.commit()
        self.session.refresh(user)

        return user

    async def delete(self, user):
        self.session.delete(user)
        self.session.commit()
        return True

    async def create(self, data: dict) -> _orm.User:
        data_user = {
            'name': data['name'],
            'email': data['username'],
            'password': data['password']
        }

        if 'role' in data:
            data_user['role'] = data['role']

        new_user = _orm.User(**data_user)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    async def attach_detach_classes(self, user_id: int, class_ids: list[int]) -> _orm.User:
        user = self.session.query(_orm.User).filter(_orm.User.id == user_id).first()
        if user:
            user.classes = []
            classes = self.session.query(_orm_classes.Classes).filter(_orm_classes.Classes.id.in_(class_ids)).all()
            for class_ in classes:
                user.classes.append(class_)
            self.session.commit()
        return user

    async def attach_detach_parse_data(self, user_id: int, parse_data_ids: list[int]) -> _orm.User:
        user = self.session.query(_orm.User).filter(_orm.User.id == user_id).first()
        if user:
            user.parse_data = []
            parse_data = self.session.query(_orm_parse_data.ParseData).filter(_orm_parse_data.ParseData.id.in_(parse_data_ids)).all()
            for data in parse_data:
                user.parse_data.append(data)
            self.session.commit()
        return user

    async def get_user_classes(self, user_id: int) -> list[_orm_classes.Classes]:
        user = self.session.query(_orm.User).filter(_orm.User.id == user_id).first()
        if user:
            return user.classes
        return []

    async def get_user_parse_data(self, user_id: int) -> list[_orm_parse_data.ParseData]:
        user = self.session.query(_orm.User).filter(_orm.User.id == user_id).first()
        if user:
            return user.parse_data
        return []