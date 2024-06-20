from config.database import Session
from repositories.classes_repository import ClassesRepository
from schemas import classes_schema as _schema

class ClassesService():
    def __init__(self, session: Session):
        self.news_repository = ClassesRepository(session)

    async def create(self, classes: _schema.ClassesInput) -> _schema.ClassesOutput:
        return await self.news_repository.create(classes)

    async def get_all(self) -> list[_schema.ClassesOutput]:
        return await self.news_repository.get_all()

    async def update(self, classes_id: int, data: _schema.ClassesInput) -> dict:
        db_classes_data = await self.news_repository.get_by_id(classes_id)

        if not db_classes_data:
            return {"success": False, "result":  "Запись не найдена"}

        is_valid = await self.news_repository.get_by_name(data.name)

        if is_valid is not None and is_valid.id != classes_id:
            return {"success": False, "result": "Запись с таким именем уже существует"}

        db_classes_data = await self.news_repository.update(db_classes_data, data)
        return db_classes_data

    async def delete(self, classes_id: int) -> dict:
        db_classes_data = await self.news_repository.get_by_id(classes_id)

        if not db_classes_data:
            return {"success": False, "result":  "Запись не найдена"}

        db_classes_data = await self.news_repository.delete(db_classes_data)
        return db_classes_data

