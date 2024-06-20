import asyncio
import json
from typing import List, Annotated, Union, Dict
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, BackgroundTasks, Form, UploadFile, File, Body
from config.database import Session
from services.auth_service import AuthService, _auth_cur_user_refresh, http_bearer

from services.disk_service import DiskService
from schemas.ml_models_schema import MlModelInput, MlModelOutput


from services.ml_model_service import MlModelService


router = APIRouter(
    prefix="/ml",
    tags=["ml"]
)

_service_auth = AuthService()
_service_file = DiskService()
_service_model = MlModelService(Session())

@router.get("/", response_model=List[MlModelOutput])
async def get_all_ml_models():
    return await _service_model.get_all()

def get_json(string: str):
    try:
        return json.loads(string)
    except:
        return {}

@router.post("/")
async def create_ml_model(ml_model: MlModelInput = Depends(), files: List[UploadFile] = File(...)):
    tasks = []
    for file in files:
        if ml_model.path_model == file.filename:
            tasks.append(asyncio.create_task(_service_file.upload(file, '/'+_service_file.dir_model + '/' + file.filename)))
        elif ml_model.path_encoder == file.filename:
            tasks.append(asyncio.create_task(_service_file.upload(file, '/'+_service_file.dir_encoder + '/' + file.filename)))
        elif ml_model.path_tokenizer == file.filename:
            tasks.append(asyncio.create_task(_service_file.upload(file, '/'+_service_file.dir_tokenizer + '/' + file.filename)))
        elif ml_model.path_sub_model == file.filename:
            tasks.append(asyncio.create_task(_service_file.upload(file, '/'+_service_file.dir_sub_model + '/' + file.filename)))

    await asyncio.gather(*tasks)

    return await _service_model.create(ml_model)


@router.put("/{ml_model_id}", response_model=MlModelOutput)
async def update_active_model(ml_model_id: int):
    await _service_model.update_active(ml_model_id)
    return await _service_model.get_by_id(ml_model_id)