import datetime as _dt
import pydantic as _pydantic


class _ClassesBase(_pydantic.BaseModel):
    name: str
    description: str | None
    is_active: bool | None = False

class ClassesInput(_ClassesBase):

    class Config:
        from_attributes = True
        orm_mode = True


class ClassesOutput(_ClassesBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True