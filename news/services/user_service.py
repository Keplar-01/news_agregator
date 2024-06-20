from config.database import Session
from passlib.context import CryptContext
from repositories.user_repisitory import UserRepository
from schemas import user_schema as _schema
from schemas import classes_schema as _schema_classes
from schemas import parse_data_schema as _schema_parse_data
from typing import List

class UserService():
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    async def get_data_user_by_id(self, id: int) -> _schema.UserOutput:
        return await self.user_repository.get_by_id(id)

    async def update(self, id: int, data: _schema.UserInput) -> _schema.UserOutput:
        db_user_data = await self.user_repository.get_by_id(id)

        if not db_user_data:
            return {"success": False, "result":  "Запись не найдена"}

        is_valid = await self.user_repository.get_by_email(data.email)

        if is_valid is not None and is_valid.id != id:
            return {"success": False, "result": "Запись с таким email уже существует"}

        db_user_data = await self.user_repository.update(db_user_data, data)

        return {"success": True, "result":  _schema.UserOutput.from_orm(db_user_data)}

    async def attach_detach_classes(self, user_id: int, class_ids: List[int]) -> _schema.UserOutput:
        return await self.user_repository.attach_detach_classes(user_id, class_ids)

    async def attach_detach_parse_data(self, user_id: int, parse_data_ids: List[int]) -> _schema.UserOutput:
        return await self.user_repository.attach_detach_parse_data(user_id, parse_data_ids)

    async def get_user_classes(self, user_id: int) -> _schema_classes.ClassesOutput:
        return await self.user_repository.get_user_classes(user_id)

    async def get_user_parse_data(self, user_id: int) -> _schema_parse_data.ParseDataOutput:
        return await self.user_repository.get_user_parse_data(user_id)

    async def create(self, data: dict) -> _schema.UserOutput:
        is_valid = await self.user_repository.get_by_email(data['username'])

        if is_valid:
            return {"success": False, "result": "Запись с таким email уже существует"}
        _bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        data['password'] = _bcrypt_context.hash(data['password'])
        return await self.user_repository.create(data)

    async def give_role(self, user_id: int, role: str) -> _schema.UserOutput:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return {"success": False, "result": "Пользователь не найден"}
        user.role = role
        user_dict = {k: v for k, v in user.__dict__.items() if not k.startswith('_')}
        update_data = _schema.UserInput(user_dict)

        await self.user_repository.update(user, update_data)