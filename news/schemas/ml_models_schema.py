import pydantic as _pydantic
from typing import Optional


class _MLModelsBase(_pydantic.BaseModel):
    name: str
    path_model: str | None = None
    path_encoder: str | None = None
    path_tokenizer: str | None = None
    path_sub_model: str | None = None
    type: str
    is_active: bool | None = None

class MlModelInput(_MLModelsBase):
    class Config:
        from_attributes = True
        orm_mode = True

class MlModelOutput(_MLModelsBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
