import datetime as _dt
from enum import Enum

import pydantic as _pydantic


class TypeUrlEnum(str, Enum):
    rss = 'rss'
    html = 'html'

class _ParserDataBase(_pydantic.BaseModel):
    url_list: str
    html_tag_list: str
    html_attr_list: str
    html_tag_element: str
    html_attr_element_type: str
    html_attr_element_value: str
    type_url: TypeUrlEnum
    to_dataset: bool
    default_class_news: str | None
    name: str


class ParseDataInput(_ParserDataBase):
    pass


class ParseDataOutput(_ParserDataBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
