import datetime as _dt
import pydantic as _pydantic


class _NewsBase(_pydantic.BaseModel):
    text: str
    title: str
    url: str
    is_train: bool
    classes: str
    name_source: str
    parse_data_id: int


class NewsInput(_NewsBase):
    date: _dt.datetime | None
    parse_data_id: int | None

    class Config:
        from_attributes = True
        orm_mode = True


class NewsOutput(_NewsBase):
    id: int
    date: _dt.datetime
    parse_data_id: int

    class Config:
        from_attributes = True
        orm_mode = True