from typing import List, Annotated, Union
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, BackgroundTasks

from config.database import Session
from services.user_service import UserService
from services.auth_service import AuthService, _auth_cur_user_access

from schemas.user_schema import UserOutput, UserInput
from schemas.classes_schema import ClassesOutput
from schemas.parse_data_schema import ParseDataOutput
from services.auth_service import oauth2_scheme, http_bearer

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(http_bearer)]
)

_service_auth = AuthService()

_service_user = UserService(Session())


@router.get("/me/",
            dependencies=[Depends(_service_auth.role_req("admin", "user"))])
async def get_by_id(user: UserOutput = Depends(_auth_cur_user_access)) -> UserOutput:
    return user

@router.get('/classes/',
dependencies=[Depends(_service_auth.role_req("admin", "user"))],
            response_model=List[ClassesOutput])
async def get_user_classes(user: UserOutput = Depends(_auth_cur_user_access)):
    return await _service_user.get_user_classes(user.id)

@router.post('/attach_classes/',
dependencies=[Depends(_service_auth.role_req("admin", "user"))],
             response_model=UserOutput)
async def attach_classes(class_ids: List[int], user: UserOutput = Depends(_auth_cur_user_access)):
    return await _service_user.attach_detach_classes(user.id, class_ids)

@router.post('/attach_parse_data/',
             dependencies=[Depends(_service_auth.role_req("admin", "user"))],
             response_model=UserOutput)
async def attach_parse_data(parse_data_ids: List[int], user: UserOutput = Depends(_auth_cur_user_access)):
    return await _service_user.attach_detach_parse_data(user.id, parse_data_ids)

@router.get('/parse_data/', dependencies=[Depends(_service_auth.role_req("admin", "user"))],
            response_model=List[ParseDataOutput])
async def get_user_parse_data(user: UserOutput = Depends(_auth_cur_user_access)):
    return await _service_user.get_user_parse_data(user.id)


@router.post('/create/', response_model=UserOutput)
async def create(data: dict):
    return await _service_user.create(data)
