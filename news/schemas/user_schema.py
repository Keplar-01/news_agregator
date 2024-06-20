import datetime as _dt
from enum import Enum

import pydantic as _pydantic


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'
    checker = 'checker'

class _UserClassesBase(_pydantic.BaseModel):
    user_id: int
    class_id: int


class UserClassesInput(_UserClassesBase):
    class Config:
        from_attributes = True
        orm_mode = True


class UserClassesOutput(_UserClassesBase):
    class Config:
        from_attributes = True
        orm_mode = True

class _UserBase(_pydantic.BaseModel):
    email: str | None = None
    name: str | None = None
    role: RoleEnum | None = RoleEnum.user


class UserInput(_pydantic.BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None
    class Config:
        from_attributes = True
        orm_mode = True

class UserOutput(_UserBase):
    id: int

    created_at: _dt.datetime

    class Config:
        from_attributes = True
        orm_mode = True


class AuthLogin(_pydantic.BaseModel):
    email: str
    password: str


class Token(_pydantic.BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
