from sqlalchemy.orm import Session
from repositories.ml_model_repository import MlModelRepository
from schemas.ml_models_schema import MlModelInput, MlModelOutput

from services.producer_service import producer_contol


class MlModelService:
    def __init__(self, session: Session):
        self.ml_model_repository = MlModelRepository(session)

    async def create(self, ml_model: MlModelInput) -> MlModelOutput:
        new_ml_model = await self.ml_model_repository.create(ml_model)
        return MlModelOutput.from_orm(new_ml_model)

    async def get_all(self) -> list[MlModelOutput]:
        all_ml_models = await self.ml_model_repository.get_all()
        return [MlModelOutput.from_orm(model) for model in all_ml_models]

    async def get_by_id(self, ml_model_id: int) -> MlModelOutput:
        ml_model = await self.ml_model_repository.get_by_id(ml_model_id)
        if not ml_model:
            return None
        return MlModelOutput.from_orm(ml_model)

    async def get_active(self) -> MlModelOutput:
        ml_model = await self.ml_model_repository.get_active()
        if not ml_model:
            return None
        return MlModelOutput.from_orm(ml_model)

    async def update(self, ml_model_id: int, data: MlModelInput) -> dict:
        db_ml_model = await self.ml_model_repository.get_by_id(ml_model_id)
        if not db_ml_model:
            return {"success": False, "result": "Запись не найдена"}

        db_ml_model = await self.ml_model_repository.update(db_ml_model, data)
        return {"success": True, "result": MlModelOutput.from_orm(db_ml_model)}

    async def delete(self, ml_model_id: int) -> dict:
        db_ml_model = await self.ml_model_repository.get_by_id(ml_model_id)
        if not db_ml_model:
            return {"success": False, "result": "Запись не найдена"}

        await self.ml_model_repository.delete(db_ml_model)
        return {"success": True, "result": "Запись удалена"}

    async def update_active(self, ml_model_id: int):
        models = await self.ml_model_repository.get_all()
        for model in models:
            if model.id == ml_model_id:
                model.is_active = True
            else:
                model.is_active = False

            model_dict = {k: v for k, v in model.__dict__.items() if not k.startswith('_')}
            update_data = MlModelInput(**model_dict)
            await self.ml_model_repository.update(model, update_data)

        model = await self.ml_model_repository.get_by_id(ml_model_id)
        message = {}
        message['command'] = 'set_model'
        message['path_model'] = model.path_model
        message['path_encoder'] = model.path_encoder
        message['path_tokenizer'] = model.path_tokenizer
        if model.path_sub_model:
            message['path_sub_model'] = model.path_sub_model
        message['type'] = model.type
        message['correlation_id'] = str(model.id)
        await producer_contol.send(message)
        return True

    async def set_active_model(self):
        model = await self.ml_model_repository.get_active()
        return await self.update_active(model.id)
