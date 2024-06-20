import datetime as _dt
import pydantic as _pydantic


class _NewsBase(_pydantic.BaseModel):
    text: str | None
    title: str | None
    url: str | None
    is_train: bool | None
    name_source: str | None
    parse_data_id: int | None
    mood: str | None


class NewsInput(_NewsBase):
    date: _dt.datetime | None
    parse_data_id: int | None
    classes_id: int | None = None

    class Config:
        from_attributes = True
        orm_mode = True


class NewsOutput(_NewsBase):
    id: int
    date: _dt.datetime
    parse_data_id: int
    classes_id: int
    classes_names: str | None = None
    class Config:
        from_attributes = True
        orm_mode = True