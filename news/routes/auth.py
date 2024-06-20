from typing import List, Annotated, Union
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, BackgroundTasks, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from config.database import Session
from services.auth_service import AuthService, _auth_cur_user_refresh, http_bearer
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from schemas import user_schema as _schema_user
from fastapi import Response
from fastapi.security import HTTPBearer

from schemas.user_schema import UserOutput



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)]
)

_service = AuthService()


@router.post('/login', response_model=_schema_user.Token)
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    token = await _service.login(username, password)
    response.set_cookie(key="access_token", value=token.access_token)
    response.set_cookie(key="refresh_token", value=token.refresh_token)
    return token


@router.post('/refresh', response_model=_schema_user.Token, response_model_exclude_none=True)
async def refresh(
        response: Response,
        user: UserOutput = Depends(_auth_cur_user_refresh),
) -> _schema_user.Token:
    token = await _service.refresh_token(user)
    response.set_cookie(key="access_token", value=token.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=token.refresh_token, httponly=True)
    return token


@router.post('/registration', response_model=_schema_user.UserOutput)
async def registration(user: _schema_user.UserInput) -> _schema_user.UserOutput:
    return await _service.register_user(user)