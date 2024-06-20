from sqlalchemy.orm import Session
from typing import List

from models.ml_models import MlModel
from schemas.ml_models_schema import MlModelInput, MlModelOutput
from repositories.interface_repository import RepositoryInterface


class MlModelRepository(RepositoryInterface):
    def __init__(self, db_session: Session):
        self.session = db_session

    async def get_all(self) -> List[MlModel]:
        return self.session.query(MlModel).all()

    async def get_by_id(self, id: int) -> MlModel:
        return self.session.query(MlModel).filter(MlModel.id == id).first()

    async def update(self, item: MlModel, data: MlModelInput) -> MlModel:
        old_value_fields = item.__dict__
        item.is_active = data.is_active

        for field in old_value_fields:
            if field in data and field != '_sa_instance_state':
                item[field] = data[field]
        self.session.commit()
        self.session.refresh(item)

        return item

    async def delete(self, item_id: int):
        self.session.delete(item_id)
        self.session.commit()

    async def create(self, item: MlModelInput) -> MlModel:
        item = MlModel(**item.dict())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    async def get_active(self) -> MlModel:
        return self.session.query(MlModel).filter(MlModel.is_active == True).first()